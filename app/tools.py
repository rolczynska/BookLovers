import json
import os
from pathlib import PosixPath

HOME = PosixPath(__file__).parent


def json_dump(var, path):
    """A function write a dictionary or list to a file."""
    with open(path, 'w') as file:
        json.dump(var, file, indent=3)


def json_load(path):
    """ A function check is the file exsists and read a file."""
    if os.path.isfile(path):
        with open(path, 'r') as file:
            content = json.load(file)
    else:
        content = {}
    return content


