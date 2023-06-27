from booklovers.parser import Book
from booklovers.mail import STATIC

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(STATIC / "ServiceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def add_to_registered(book: Book, email: str):
    """
    Adds this book and email to Firestore database.
    """
    data = {"title": f"{book.title}",
            "author": f"{book.author}",
            "url": f"{book.url}",
            "emails": [f'{email}']
            }
    db.collection('books').document(f'{book.title}+{book.author}').set(data)


def get_registered_books(email: str) -> list:
    """
   Gets list of books registered for this email.
        """
    pass


def get_book(book_title, book_author) -> Book:
    """
    Gets Book object from database.
        """
    pass


def is_new_subscription(book: Book, email: str) -> bool:
    """Returns True if the Book and email are new subscription."""
    pass


def remove_email(book: Book, email: str):
    """Function remove book from notification list. """
    # demanded_books = get_registered_books(email)
    # if book in demanded_books:
    #     demanded_books[book].remove(email)
    #     if len(demanded_books[book]) == 0:
    #         demanded_books.pop(book)
    # # remove book from database
