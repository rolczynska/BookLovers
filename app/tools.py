import json
from pathlib import PosixPath
from urllib.parse import unquote
import os
HOME = PosixPath(__file__).parent


def add_to_list(title, email, path):
    """Function check is that file exist, load content and add title and email to file."""
    if os.path.isfile(path):
        searching_books = json_load(path)
    else:
        searching_books = {}
    if title in searching_books:
        searching_books[title].append(email)
    else:
        searching_books[title] = email
    json_dump(searching_books, path)


def is_already_registered(title, email, path):
    """Function load content of file and check if this title and email is already registered."""
    if os.path.isfile(path):
        content = json_load(path)
        if title in content:
            if email in content[title]:
                return True
    return False


def delete_from_searching_book_file(titles_to_delete, path):
    file = json_load(path)
    for title in titles_to_delete:
        file.pop(title)
    json_dump(file, path)


def decode(string: str):
    address, key_value_pair = string.split('?')
    key, value = key_value_pair.split('=')
    return ' '.join(unquote(value).split('+'))


def json_dump(var, file_path):
    """A function write a dictionary or list to a file."""
    with open(file_path, 'w') as file:
        json.dump(var, file, indent=3)


def json_load(file_path):
    """ A function read a file."""
    with open(file_path, 'r') as file:
        return json.load(file)
