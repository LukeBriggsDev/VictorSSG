import os
import shutil
from jinja2 import Environment, PackageLoader, select_autoescape

# Directories
content_dir = os.path.join(os.getcwd(), "content")
static_dir = os.path.join(os.getcwd(), "static")
public_dir = os.path.join(os.getcwd(), "public")
archetypes_dir = os.path.join(os.getcwd(), "archetypes")

config_file = os.path.join(os.getcwd(), "config.yaml")

# Jinja environment
jinja_env = Environment(
    loader=PackageLoader("victor"),
    autoescape=select_autoescape()
)
