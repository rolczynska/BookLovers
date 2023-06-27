from booklovers.parser import Book
from booklovers.mail import STATIC

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import firestore as firestr


cred = credentials.Certificate(STATIC / "ServiceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def add_to_registered(book: Book, email: str):
    """Adds this book and email to Firestore database."""

    id = f'{book.author} "{book.title}"'
    book_ref = db.collection('books').document(id)
    if not book_ref.get().exists:
        data = {"title": f"{book.title}",
                "author": f"{book.author}",
                "url": f"{book.url}",
                "emails": [f'{email}']
                }
        db.collection('books').document(f'{book.author}-"{book.title}"').set(data)
    book_ref.update({'emails': firestr.ArrayUnion([email])})


def remove_email(title: str, author: str, email: str):
    """Function remove book from notification list. """
    book_ref = db.collection('books').document(f'{author} "{title}"')
    book_ref.update({'emails': firestr.ArrayRemove([email])})


def delete_book(title: str, author: str):
    """Delete book from database."""
    pass


def get_registered_books(email: str) -> list:
    """
   Gets list of books registered for this email.
        """
    pass

