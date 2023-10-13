from booklovers.forms import Search
from booklovers.mail import STATIC

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import firestore as firestr


cred = credentials.Certificate(STATIC / "ServiceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def add_to_registered(search: Search):
    """ Adds this book and email to Firestore database. """
    book_id = f'{search.author} "{search.title}"'
    book_ref = db.collection('books').document(book_id)
    if not book_ref.get().exists:
        book_data = {"title": f"{search.title}",
                     "author": f"{search.author}"}
        book_ref.set(book_data)
    for library in search.libraries:
        lib_ref = book_ref.collection('libraries').document(f"{library}")
        if lib_ref.get().exists:
            lib_ref.update({'emails': firestr.ArrayUnion([search.email])})
        else:
            book_ref.collection('libraries').document(f"{library}").set({'emails': [search.email]})


def remove_email(title: str, author: str, email: str):
    """ Function remove book from notification list. """
    book_ref = db.collection('books').document(f'{author} "{title}"')
    book_ref.update({'emails': firestr.ArrayRemove([email])})


def get_registered_books(email: str) -> list:
    """ Gets list of books registered for this email. """
    books = db.collection('books').where('emails', 'array_contains', email).get()
    result = [book.libraries_and_mails_to_dict() for book in books]
    return result


