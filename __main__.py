"""Main method"""
import math
import socketserver
import sys
import os
import shutil
from datetime import datetime
from typing import Tuple
import regex as re
import pathlib
import yaml
from jinja2 import Environment, PackageLoader, select_autoescape
import mistune
from .CONSTANTS import content_dir, static_dir, jinja_env, public_dir, CONFIG, archetypes_dir, yaml_re, eval_re, \
    code_re, header_re
from .social.social import DefaultSites, SocialLink
from http.server import HTTPServer, SimpleHTTPRequestHandler
from .MarkdownDocument import MarkdownDocument


def init():
    """Initialise directory for use"""
    # Copy config files
    shutil.copy(os.path.join(os.path.dirname(__file__), "proto", "config.yaml"), os.getcwd())

    # Copy archetype
    shutil.copytree(os.path.join(os.path.dirname(__file__), "proto", "archetypes"),
                    os.path.join(os.getcwd(), "archetypes"))

    # Create directories if not exist
    for directory in [content_dir, static_dir, public_dir, archetypes_dir]:
        if not os.path.exists(directory):
            os.mkdir(directory)


def build():
    """Build webpage into public directory"""
    try:

        # Remove existing build
        if os.path.exists(public_dir):
            shutil.rmtree(public_dir)
            os.mkdir(public_dir)

        # Non-empty social links
        config_links = CONFIG["index"]["socialLinks"]

        # Links to appear on page
        social_links = []
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

        # Copy stylesheets
        shutil.copytree(os.path.join(os.path.dirname(__file__), "assets"), os.path.join(public_dir,
                                                                                        "assets"))
        # Copy static
        shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)

        # Build index
        index_page = jinja_env.get_template("index.html")
        with open(os.path.join(public_dir, "index.html"), "w") as f:
            f.write(index_page.render(CONFIG=CONFIG, social_links=social_links))

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
            shutil.copy(file, directory)
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
                dest.write(template.render(CONFIG=CONFIG, page_title=page.title(), post=document))

        # Arrange posts page
        posts = []
        for document in documents:
            if public_dir.joinpath("posts") in document.path.parents:
                posts.append(document)
        posts.sort(key=lambda x: datetime.timestamp(x.date), reverse=True)
        # Render post pages
        with open(public_dir.joinpath("posts/index.html"), "w") as post_page:
            post_page.write(jinja_env.get_template("posts/list.html").render(CONFIG=CONFIG, page_title="Posts",
                                                                             posts=posts[:16], public_dir=public_dir,
                                                                             next_page="posts/1", prev_page=None))

        for i in range(math.ceil(len(posts) / 16)):
            page = public_dir.joinpath(f"posts/{i}")
            next_page  = f"posts/{i + 1}" if (i + 1) < math.ceil(len(posts) / 16) else None
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

    # except KeyError as e:
    #     print(f"{e.args[0]} was not found in config, please add this field or reinitialise")


class HTTPHandler(SimpleHTTPRequestHandler):
    """Simple HTTPS handler to serve from public directory"""

    def __init__(self, *args,
                 **kwargs):
        root_path = os.path.join(os.getcwd(), "public")
        super().__init__(*args, directory=root_path, **kwargs)


def serve():
    """Run basic web server in directort"""
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, HTTPHandler)
    print("Stating server on http://127.0.0.1:8000.\n Close with ^C")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nClosing server")
        exit(0)


def new():
    if len(sys.argv) != 3:
        print("No path detected. Please run \n`new path/to/file.md`")
        exit(0)

    new_file = os.path.join(content_dir, sys.argv[2])

    # Make parent directories
    os.makedirs(os.path.dirname(new_file), exist_ok=True)

    # Copy correct archetype for extension
    file_ext = os.path.basename(new_file).split(".")[-1]

    try:
        if os.path.exists(new_file):
            raise shutil.SameFileError
        # Evaluate any inline python in yaml header
        with open(os.path.join(archetypes_dir, f"default.{file_ext}")) as archetype, open(new_file, "w") as dest:
            header = re.findall(header_re, archetype.read())[0]
            new_header = ""
            # Evaluate python in yaml fields and replace
            for match in re.finditer(eval_re, header):
                replacement = eval(match.group())
                new_header = re.sub(code_re, replacement, header)
                break
            dest.write(new_header)

    except FileNotFoundError:
        # archetype for file type does not exist
        pathlib.Path(new_file).touch()

    except shutil.SameFileError:
        print("File already exists")
        exit()


def help():
    """Provide help message listing commands"""
    help_messages = {
        "help": "display this message",
        "init": "initialise directory for victor project",
        "build": "build directory",
        "serve": "start basic web server",
        "new FILE": "create a new file with content of archetype"
    }
    print("Available commands:")
    # Whitespace between command and description
    col_gap = 16
    for command in help_messages.keys():
        print(f"  {command}{' ' * (col_gap - len(command))}{help_messages[command]}")


# Program arguments
if len(sys.argv) == 1:
    build()

elif sys.argv[1] == "init":
    init()

elif sys.argv[1] == "serve":
    serve()

elif sys.argv[1] == "new":
    new()

else:
    help()
