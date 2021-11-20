import os
import pathlib

import regex as re
import yaml
from jinja2 import Environment, PackageLoader, select_autoescape

# Directories
content_dir = pathlib.Path(os.path.join(os.getcwd(), "content"))
static_dir = pathlib.Path(os.path.join(os.path.join(os.getcwd(), "static")))
public_dir = pathlib.Path(os.path.join(os.path.join(os.getcwd(), "public")))
archetypes_dir = pathlib.Path(os.path.join(os.path.join(os.getcwd(), "archetypes")))

config_file = pathlib.Path(os.path.join(os.getcwd(), "config.yaml"))
# Config
with open(config_file, "r") as f:
    CONFIG = yaml.safe_load(f.read())

# Jinja environment
jinja_env = Environment(
    loader=PackageLoader("victor"),
    autoescape=select_autoescape()
)

# REGEX
# whole header including '---' delimiter
header_re = re.compile(r"^-{3}\n[\w\W]+?-{3}")
# header without '---' delimiter
yaml_re = re.compile(r"(?<=^-{3})\n[\w\W]+?(?=-{3})")
# code to be eval in evaluation block
eval_re = re.compile(r"(?<={{)([^{{}}]*)(?=}})")
# whole code including '{{' '}}'
code_re = re.compile(r"({{[^{{}}]*}})")

