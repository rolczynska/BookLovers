import tools
from tools import json_load, json_dump


def get_id(title: str, path: str, author=None, url=None) -> str:
    """
    This function takes a book title, optional author, and a path to a JSON file representing a book
    index. It returns the ID of the corresponding book in the index. If the book is not found,
    a new ID is generated and the book is added to the index with the provided information.
       """
    books_ids = tools.json_load(path)
    for book_id, info in books_ids.items():
        if info.get("title") == title or info.get("author") == author:
            return book_id
    book_id = str(len(books_ids.keys()) + 1)
    books_ids[book_id] = {"title": title, "author": author, "url": url}
    tools.json_dump(books_ids, path)
    return book_id


def add_to_demanded_list(book_id: str, email: str, path: str) -> bool:
    """
    This function adds a book ID and email to a JSON file called "demanded_books", which maintains
    a list of books currently being searched for by users. It returns True if the book and email are
    successfully added to the list. If the email is already associated with the specified book ID in
    the "demanded_books" file, it returns False without modifying the file.
    """
    demanded_books = json_load(path)
    if book_id in demanded_books:
        emails = demanded_books.get(book_id)
        if email in emails:
            return False
        demanded_books[book_id].append(email)
    else:
        demanded_books[book_id] = [email]
    json_dump(demanded_books, path)
    return True


def get_books(some_books_id: list) -> list:
    """
    This function retrieves information about a list of books specified by their IDs.
    It expects the book IDs to be passed as a list of strings. It retrieves the book information
    from a JSON file called "books_index.json" located in the home directory of the current user.
    The function returns the information as a list of lists, where each sublist contains the title
    and author of a book specified by the corresponding book ID in the input list.
        """
    books_info = []
    all_books_ids = json_load(path=tools.HOME / "books_index.json")
    for book_id in some_books_id:
        book_info = [all_books_ids[book_id].get("title"),
                     all_books_ids[book_id].get("author")]
        books_info.append(book_info)
    return books_info


def get_registered_books(email: str) -> list:
    """
    This function retrieves a list of book titles and authors registered for a given email address.
    It expects the email address as a string and retrieves the information from a JSON file called
    "demanded_books.json" in the user's home directory. The function returns a list of book titles
    and authors for the specified email address. If the email address is not found, an empty list
    is returned.
        """
    demanded_books_id = []
    books = json_load(path=tools.HOME / "demanded_books.json")
    for book_id, emails in books.items():
        if email in emails:
            demanded_books_id.append(book_id)
    registered_books = get_books(demanded_books_id)
    return registered_books
