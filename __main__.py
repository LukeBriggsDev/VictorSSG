"""Main method"""
import sys
import os
import shutil
import json
from jinja2 import Environment, PackageLoader, select_autoescape
from .CONSTANTS import content_dir, static_dir, jinja_env, public_dir, config_file


def init():
    """Initialise directory for use"""
    # Copy config files
    shutil.copy(os.path.join(os.path.dirname(__file__), "proto", "config.json"), os.getcwd())

    # Create directory if not exist
    for directory in [content_dir, static_dir, public_dir]:
        if not os.path.exists(directory):
            os.mkdir(directory)


def build():
    """Build webpage into public directory"""
    # Config
    try:
        with open(config_file, "r") as f:
            CONFIG = json.loads(f.read())

        index_page = jinja_env.get_template("base.html")
        with open(os.path.join(public_dir, "index.html"), "w") as f:
            f.write(index_page.render(title=CONFIG['title']))

    except FileNotFoundError as e:
        print(f"{e.filename} was not found, have you ran init?")


def help():
    """Provide help message listing commands"""
    help_messages={
        "help": "display this message",
        "init": "initialise directory for victor project",
        "build": "build directory"
    }
    print("Available commands:")
    for command in help_messages.keys():
        print(f"  {command}\t\t{help_messages[command]}")

# Program arguments
if len(sys.argv) == 1:
    build()

elif sys.argv[1] == "init":
    init()

else:
    help()


