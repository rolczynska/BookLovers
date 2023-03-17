import tools
from tools import json_load, json_dump


def get_id(title, author, url, path):
    """Function return an id from books_index for specific title and author."""
    books_ids = tools.json_load(path)
    for id, info in books_ids.items():
        if info.get("title") == title or info.get("author") == author:
            return id
    id = str(len(books_ids.keys()) + 1)
    books_ids[id] = {"title": title, "author": author, "url": url}
    tools.json_dump(books_ids, path)
    return id


def add_to_searching_list(id, email, path):
    """Function load content and book_id and email to a searching_books file."""
    searching_books = json_load(path)
    if id in searching_books:
        emails = searching_books.get(id)
        if email in emails:
            return False
        searching_books[id].append(email)
    else:
        searching_books[id] = [email]
    json_dump(searching_books, path)
    return True


# TODO te funkcje trzeba sprawdzić
def get_books_from_ids(some_books_id):
    """Function take list of some books id and return list of books - titles, author, url."""
    searching_books = []
    all_books_ids = json_load(path=tools.HOME / "books_id.json")
    for book_id in some_books_id:
        book_info = [all_books_ids[book_id].get("title"), all_books_ids[book_id].get("author")]
        searching_books.append(book_info)
    return searching_books


def registered_books(email):
    """Function take email and return list of registered book id for that email."""
    searching_books_id = []
    content = json_load(path=tools.HOME / "searching_books.json")
    for book_id, emails in content.items():
        if email in emails:
            searching_books_id.append(book_id)
    searching_books = get_books_from_ids(searching_books_id)
    return searching_books

