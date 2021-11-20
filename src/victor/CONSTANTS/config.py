import pathlib
import yaml
import os

config_file = pathlib.Path(os.path.join(os.getcwd(), "config.yaml"))
# Config
with open(config_file, "r") as f:
    CONFIG = yaml.safe_load(f.read())