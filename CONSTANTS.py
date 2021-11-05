import os
import shutil
from jinja2 import Environment, PackageLoader, select_autoescape
import json

# Directories
content_dir = os.path.join(os.getcwd(), "content")
static_dir = os.path.join(os.getcwd(), "static")
public_dir = os.path.join(os.getcwd(), "public")

config_file = os.path.join(os.getcwd(), "config.json")

# Jinja environment
jinja_env = Environment(
    loader=PackageLoader("victor"),
    autoescape=select_autoescape()
)
