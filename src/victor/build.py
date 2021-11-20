import glob
import math
import os
import shutil
from datetime import datetime
from datetime import timezone

import regex as re
import yaml
from feedgen.feed import FeedGenerator

from .CONSTANTS.directories import content_dir, static_dir, public_dir
from .CONSTANTS.environment import jinja_env
from .CONSTANTS.config import CONFIG
from .CONSTANTS.regex import yaml_re, header_re
from .MarkdownDocument import MarkdownDocument
from .social.social import DefaultSites, SocialLink


def build():
    """Build webpage into public directory"""
    try:
        # Remove existing build
        files_to_remove = glob.glob(str(public_dir.relative_to(os.getcwd()).joinpath("**")))
        if os.path.exists(public_dir):
            for file in files_to_remove:
                try:
                    shutil.rmtree(file)
                except NotADirectoryError:
                    os.remove(file)

        # Non-empty social links
        config_links = CONFIG["index"]["socialLinks"]

        # Links to appear on page
        social_links = []
        other_links = []
        for link in config_links:
            if config_links[link] != "":
                if link == "linkedin":
                    social_links.append(SocialLink(DefaultSites.LINKEDIN, config_links["linkedin"]))
                elif link == "github":
                    social_links.append(SocialLink(DefaultSites.GITHUB, config_links["github"]))
                elif link == "gitlab":
                    social_links.append(SocialLink(DefaultSites.GITLAB, config_links["gitlab"]))
                elif link == "twitter":
                    social_links.append(SocialLink(DefaultSites.TWITTER, config_links["twitter"]))
                else:
                    other_links.append({"icon": "fa-"+link, "link": config_links[link]})





        # Copy stylesheets
        shutil.copytree(os.path.join(os.path.dirname(__file__), "assets"), os.path.join(public_dir,
                                                                                        "assets"))
        # Copy static
        shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)

        # Build index
        index_page = jinja_env.get_template("index.html")
        with open(os.path.join(public_dir, "index.html"), "w") as f:
            f.write(index_page.render(CONFIG=CONFIG, social_links=social_links, other_links=other_links))

        # Create sitemap.xml
        with open(public_dir.joinpath("sitemap.xml"), "w") as sitemap:
            sitemap.write("""<urlset
xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
xmlns:xhtml="http://www.w3.org/1999/xhtml">""")

        # Build content
        content_files = content_dir.glob("**/*.md")
        # List of converted documents
        documents = []
        for file in content_files:
            page = file.stem
            # Place html in directory with name of page
            directory = public_dir.joinpath(file.relative_to(content_dir).parent.joinpath(page))
            os.makedirs(directory, exist_ok=True)
            # Copy original file to be accessed at index.md
            shutil.copy(file, os.path.join(directory, "index.md"))
            # Export file
            html_export = directory.joinpath("index.html")
            # Convert markdown (without yaml header) to html
            with open(file, "r") as src, open(os.path.join(public_dir, html_export), "w") as dest:
                markdown = src.read()

                yaml_data = re.findall(yaml_re, markdown)[0]
                header = re.findall(header_re, markdown)[0]
                text = markdown.replace(header, "")
                metadata = yaml.safe_load(yaml_data)
                document = MarkdownDocument(path=directory.joinpath(file.name), markdown=text, metadata=metadata)
                documents.append(document)

                if content_dir.joinpath("projects") in file.parents or content_dir.joinpath("posts") in file.parents:
                    template = jinja_env.get_template("posts/post.html")
                else:
                    template = jinja_env.get_template("info.html")
                dest.write(template.render(CONFIG=CONFIG, page_title=metadata["title"], post=document))

                # Add to sitemap
                with open(public_dir.joinpath("sitemap.xml"), "a") as sitemap:
                    sitemap.write(
                        f"""
    <url>
        <loc>{CONFIG["base_url"]}{directory.relative_to(public_dir)}/</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.5</priority>
    </url>
                                """)

        with open(public_dir.joinpath("sitemap.xml"), "a") as sitemap:
            # close sitemap
            sitemap.write("</urlset>")


        # Arrange posts page
        posts = []
        for document in documents:
            if public_dir.joinpath("posts") in document.path.parents:
                posts.append(document)

        posts.sort(key=lambda x: datetime.timestamp(x.date), reverse=True)

        # Create rss feed
        fg = FeedGenerator()
        fg.title(CONFIG["title"])
        fg.link(href=CONFIG["base_url"], rel='alternate')
        fg.author(name=CONFIG["name"], email=CONFIG["email"])
        fg.logo(str(public_dir.joinpath("favicon.ico")))
        fg.subtitle(CONFIG["description"])
        fg.language("en")

        for post in posts:
            fe = fg.add_entry()
            fe.id = CONFIG["base_url"] + str(post.path.relative_to(public_dir))
            fe.link(href=CONFIG["base_url"] + str(post.path.relative_to(public_dir)))
            # Remove html tags
            fe.title(title=re.sub('<[^<]+?>', '', post.title))
            fe.description(post.html if post.rss_full_text else post.description)
            fe.author(name=post.author)
            fe.content(post.html)
            fe.pubDate(post.date.replace(tzinfo=timezone.utc))
            fg.rss_file(str(public_dir.joinpath("index.xml")), pretty=True)

        # Render post pages
        with open(public_dir.joinpath("posts/index.html"), "w") as post_page:
            next_page = f"posts/1" if 1 < math.ceil(len(posts) / 16) else None
            post_page.write(jinja_env.get_template("posts/list.html").render(CONFIG=CONFIG, page_title="Posts",
                                                                             posts=posts[:16], public_dir=public_dir,
                                                                             next_page=next_page, prev_page=None))

        # Creat 'next' amd 'previous' links
        for i in range(math.ceil(len(posts) / 16)):
            page = public_dir.joinpath(f"posts/{i}")
            next_page = f"posts/{i + 1}" if (i + 1) < math.ceil(len(posts) / 16) else None
            prev_page = f"posts/{i - 1}" if (i - 1) >= 0 else None
            os.makedirs(page)
            with open(page.joinpath("index.html"), "w") as project_page:
                project_page.write(
                    jinja_env.get_template("posts/list.html").render(CONFIG=CONFIG, page_title="Posts",
                                                                     posts=posts[(i * 16):(i + 1) * 16],
                                                                     public_dir=public_dir,
                                                                     next_page=next_page,
                                                                     prev_page=prev_page))

        # Arrange projects page
        projects = []
        for document in documents:
            if public_dir.joinpath("projects") in document.path.parents:
                projects.append(document)
        projects.sort(key=lambda x: datetime.timestamp(x.date), reverse=True)
        # Render project page
        with open(public_dir.joinpath("projects/index.html"), "w") as project_page:
            project_page.write(jinja_env.get_template("projects/list.html").render(CONFIG=CONFIG, page_title="Projects",
                                                                                   projects=projects,
                                                                                   public_dir=public_dir))
    except FileNotFoundError as e:
        print(f"{e.filename} was not found, have you ran init?")

    except KeyError as e:
        print(f"{e.args[0]} was not found in config, please add this field or reinitialise")
