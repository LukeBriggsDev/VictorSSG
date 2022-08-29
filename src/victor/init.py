import os
import shutil

from .CONSTANTS.directories import content_dir, static_dir, public_dir, archetypes_dir


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