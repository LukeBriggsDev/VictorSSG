import os
import pathlib
import shutil
import sys

import regex as re

from .CONSTANTS.directories import content_dir, archetypes_dir, eval_re
from .CONSTANTS.regex import code_re, header_re


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
