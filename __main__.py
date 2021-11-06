"""Main method"""
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
from .CONSTANTS import content_dir, static_dir, jinja_env, public_dir, config_file, archetypes_dir, yaml_re, eval_re, \
    code_re, header_re
from .social.social import DefaultSites, SocialLink
from http.server import HTTPServer, SimpleHTTPRequestHandler


def init():
    """Initialise directory for use"""
    # Copy config files
    shutil.copy(os.path.join(os.path.dirname(__file__), "proto", "config.yaml"), os.getcwd())

    # Copy archetype
    shutil.copytree(os.path.join(os.path.dirname(__file__), "proto", "archetypes"), os.path.join(os.getcwd(), "archetypes"))

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

        # Config
        with open(config_file, "r") as f:
            CONFIG = yaml.safe_load(f.read())


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
        # Build index
        index_page = jinja_env.get_template("index.html")
        with open(os.path.join(public_dir, "index.html"), "w") as f:
            f.write(index_page.render(site_title=CONFIG['title'], navbar=CONFIG["navbar"], social_links=social_links))

        # Build content
        content_files = pathlib.Path(content_dir).glob("**/*.md")
        for file in content_files:
            page = '.'.join(file.name.split('.')[:-1])
            # Place html in directory with name of page
            directory = file.parent.relative_to(content_dir).parent.joinpath(page)
            os.makedirs(os.path.join(public_dir, directory), exist_ok=True)
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

                # Evaluate python in yaml fields and replace
                for match in re.finditer(eval_re, yaml_data):
                    replacement = eval(match.group())
                    yaml_data = re.sub(code_re, replacement, yaml_data)
                    break

                metadata = yaml.safe_load(yaml_data)
                template = jinja_env.get_template("info_page.html")
                dest.write(template.render(site_title=CONFIG["title"], page_title=page.title(),navbar=CONFIG["navbar"], page_content=mistune.markdown(text, escape=False)))

    except FileNotFoundError as e:
        print(f"{e.filename} was not found, have you ran init?")

    except KeyError as e:
        print(f"{e.args[0]} was not found in config, please add this field or reinitialise")


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


def help():
    """Provide help message listing commands"""
    help_messages={
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
        shutil.copy(os.path.join(archetypes_dir, f"default.{file_ext}"), new_file)

    except FileNotFoundError:
        # archetype for file type does not exist
        pathlib.Path(new_file).touch()

    except shutil.SameFileError:
        print("File already exists")
        exit()


else:
    help()


