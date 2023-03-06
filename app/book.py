import tools
from tools import json_load, json_dump


def is_in_books_index(title, author, path):
    """Function check is searching book in books_index. Return boolean."""
    books_ids = tools.json_load(path)
    for id, info in books_ids.items():
        if info.get("title") == title and info.get("author") == author:
            return True
    return False


def get_id(title, author, path):
    """Function return an id from books_index for specific title and author."""
    books_ids = tools.json_load(path)
    result = ""
    for id, info in books_ids.items():
        if info.get("title") == title and info.get("author") == author:
            result = id
    return result


def get_next_id(books_ids):
    """Function generate a next id for new book."""
    return str(len(books_ids.keys()) + 1)


def add_to_books_index(title, author, url, path):
    books_ids = tools.json_load(path=tools.HOME / "books_index.json")
    book_id = get_next_id(books_ids)
    books_ids[book_id] = {"title": title, "author": author, "url": url}
    tools.json_dump(books_ids, path)
    return book_id


def add_to_searching_list(book_id, email, path):
    """Function load content and book_id and email to a file."""
    searching_books = json_load(path)
    if book_id in searching_books:
        searching_books[book_id].append(email)
    else:
        searching_books[book_id] = [email]
    json_dump(searching_books, path)


def is_mail_registered(book_id, email) -> bool:
    """Function check if this email is already registered for that book_id."""
    searching_books = json_load(path=tools.HOME / "searching_books.json")
    if book_id in searching_books:
        emails = searching_books.get(book_id)
        if email in emails:
            return True
    return False


def get_books_from_ids(some_books_id):
    """Funtion take list of some books id and return list of books - titles, author, url."""
    searching_books = []
    all_books_ids = json_load(path=tools.HOME / "books_id.json")
    for book_id in some_books_id:
        book_info = []
        book_info.append(all_books_ids[book_id].get("title"))
        book_info.append(all_books_ids[book_id].get("author"))
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


