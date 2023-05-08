import tools
from tools import json_load, json_dump


def get_id(title, path, author=None, url=None) -> str:
    """
       Given a book title, author (optional), and a path to a JSON file representing a book index,
       this function returns the ID of the corresponding book in the index.

       Args:
           title (str): The title of the book to search for.
           path (str): The path to the JSON file representing the book index.
           author (str, optional): The author of the book to search for. Defaults to None.
           url (str, optional): The URL of the book to search for. Defaults to None.

       Returns:
           str: The ID of the book in the index. If the book is not found, a new ID is generated and
           the book is added to the index with the provided information.

       Raises:
           IOError: If the JSON file cannot be read or written to.

       """
    books_ids = tools.json_load(path)
    for book_id, info in books_ids.items():
        if info.get("title") == title or info.get("author") == author:
            return book_id
    book_id = str(len(books_ids.keys()) + 1)
    books_ids[book_id] = {"title": title, "author": author, "url": url}
    tools.json_dump(books_ids, path)
    return book_id


def add_to_demanded_list(book_id, email, path):
    """
    Load the specified book ID and email into the searching_books file.

    Args:
        book_id (str): The ID of the book to add to the searching list.
        email (str): The email address of the user searching for the book.
        path (str): The file path of the searching_books JSON file.

    Returns: bool: True if the book and email were successfully added to the list, False if the
    email was already saved.

    Raises:
        JSONDecodeError: If the searching_books file cannot be decoded as JSON.
        JSONEncodeError: If the searching_books file cannot be encoded as JSON.

    The `searching_books` file is a JSON file that maintains a list of books that are currently
    being searched for by users. This function adds the specified book ID and email to the list,
    and returns True if the operation is successful. If the specified email is already associated
    with the specified book ID in the searching_books file, the function returns False without
    modifying the file.
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


def get_books(some_books_id):
    """
        Retrieve information about a list of books specified by their IDs.

        Args:
            some_books_id (List[str]): A list of book IDs to retrieve information about.

        Returns:
            List[List[str]]: A list of lists, where each sublist contains the title and author of
            a book
            specified by the corresponding book ID in the input list.

        Raises:
            JSONDecodeError: If the books_index file cannot be decoded as JSON.

        This function retrieves information about a list of books specified by their IDs,
        and returns the information
        as a list of lists, where each sublist contains the title and author of a book. The
        function expects the book IDs to be passed in as a list of strings.

        The function retrieves book information from a JSON file called `books_index.json`,
        located in the home directory
        of the current user. The file should contain a mapping of book IDs to book information,
        where each book entry is
        a dictionary containing keys for the book's title, author, and other metadata.
        """
    books_info = []
    all_books_ids = json_load(path=tools.HOME / "books_index.json")
    for book_id in some_books_id:
        book_info = [all_books_ids[book_id].get("title"),
                     all_books_ids[book_id].get("author")]
        books_info.append(book_info)
    return books_info


def get_registered_books(email):
    """
        Retrieve a list of book titles and authors that are registered for a given email address.

        Args:
            email (str): A string representing the email address to look up.

        Returns:
            List[List[str]]: A list of lists, where each sublist contains the title and author of
            a book
            registered for the specified email address.

        Raises:
            JSONDecodeError: If the demanded_books file cannot be decoded as JSON.

        This function takes an email address as input, and returns a list of book titles and
        authors that are registered
        for that email address. The function expects the email address to be passed in as a string.

        The function retrieves the list of books and associated email addresses from a JSON file
        called `demanded_books.json`,
        located in the home directory of the current user. The file should contain a mapping of
        book IDs to lists of email
        addresses that have registered interest in those books.

        If the specified email address is not found in the file, the function returns an empty
        list. If the file cannot be
        decoded as JSON, a `JSONDecodeError` is raised.
        """
    demanded_books_id = []
    books = json_load(path=tools.HOME / "demanded_books.json")
    for book_id, emails in books.items():
        if email in emails:
            demanded_books_id.append(book_id)
    registered_books = get_books(demanded_books_id)
    return registered_books
