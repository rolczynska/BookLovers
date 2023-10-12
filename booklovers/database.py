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
    data = search.libraries
    db.collection('books').document(book_id).set(data)


def make_libraries_collection(search, book_ref):
    for library in search.libraries:
        library_id = f"{library}"
        library_ref = book_ref.collection('libraries').document(library_id)
        book = book_ref.get()
        if book_ref.exsists:
            library_ref.update({'emails': firestr.ArrayUnion([search.email])})
        library_ref.set({'emails': [f"{search.email}"]})



def remove_email(title: str, author: str, email: str):
    """ Function remove book from notification list. """
    book_ref = db.collection('books').document(f'{author} "{title}"')
    book_ref.update({'emails': firestr.ArrayRemove([email])})


def get_registered_books(email: str) -> list:
    """ Gets list of books registered for this email. """
    books = db.collection('books').where('emails', 'array_contains', email).get()
    result = [book.to_dict() for book in books]
    return result


add_to_registered(search=Search(title="Dziewczynka z zapałkami", author="ola O.",
                                libraries={"marcinkowskiego": ["olkiewiczka@ail.pl",
                                                               "blablabla@kiiis.pl"],
                                           "jackowskiego": ["buziaczke@mail.pl"]}))

