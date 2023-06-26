from booklovers.parser import Book


def get_book(book_title, book_author) -> Book:
    """
    Gets Book object from database.
        """
    pass


def is_new_subscription(book: Book, email: str) -> bool:
    """Returns True if the Book and email are new subscription."""
    pass


def get_registered_books(email: str) -> list:
    """
   Gets list of books registered for this email.
        """
    pass


def add_to_registered(book: Book, email: str) -> bool:
    """
    Adds this book and email to database.
    """
    pass


def remove_email(book: Book, email: str):
    """Function remove book from notification list. """
    # demanded_books = get_registered_books(email)
    # if book in demanded_books:
    #     demanded_books[book].remove(email)
    #     if len(demanded_books[book]) == 0:
    #         demanded_books.pop(book)
    # # remove book from database


