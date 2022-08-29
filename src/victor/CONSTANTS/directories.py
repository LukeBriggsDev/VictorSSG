import os
import pathlib

content_dir = pathlib.Path(os.path.join(os.getcwd(), "content"))
static_dir = pathlib.Path(os.path.join(os.path.join(os.getcwd(), "static")))
public_dir = pathlib.Path(os.path.join(os.path.join(os.getcwd(), "public")))
archetypes_dir = pathlib.Path(os.path.join(os.path.join(os.getcwd(), "archetypes")))