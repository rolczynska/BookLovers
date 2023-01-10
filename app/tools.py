import json
import os
from pathlib import PosixPath

HOME = PosixPath(__file__).parent


def json_dump(var, file_path):
    """A function write a dictionary or list to a file."""
    with open(file_path, 'w') as file:
        json.dump(var, file, indent=3)


def json_load(file_path):
    """ A function read a file."""
    with open(file_path, 'r') as file:
        return json.load(file)


def add_to_list(title, email, path):
    """Function check is that file exist, load content and add title and email to a file."""
    if os.path.isfile(path):
        searching_books = json_load(path)
    else:
        searching_books = {}
    if title in searching_books:
        searching_books[title].append(email)
    else:
        searching_books[title] = [email]
    json_dump(searching_books, path)


def is_already_registered(title, email, path) -> bool:
    """Function check if this title and email is already registered."""
    if os.path.isfile(path):
        content = json_load(path)
        if title in content:
            if email in content[title]:
                return True
    return False


def remove_email(title, email, path=HOME / 'searching_books.json'):
    if os.path.isfile(path):
        searching_books = json_load(path)
        try:
            searching_books[title].remove(email)
            if len(searching_books[title]) == 0:
                searching_books.pop(title)
        except (KeyError, ValueError):
            json_dump(searching_books, path)
    else:
        searching_books = {}
    json_dump(searching_books, path)


