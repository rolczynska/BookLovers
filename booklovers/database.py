from google.cloud.firestore_v1 import FieldFilter

from booklovers.forms import Book, Mail, Search
from booklovers.mail import STATIC
from booklovers.parser import is_free
from booklovers.connect import get_libraries_availability
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import firestore as firestr


cred = credentials.Certificate(STATIC / "ServiceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def get_users() -> list[str]:
    """ Return all signed users emails """
    users = set()
    searches = get_searches()
    for search in searches:
        users.add(search.email)
    return users


def get_mail_obj(user) -> Mail:
    """ Return Mail obj contain email and list of Books available"""
    books = []
    searches = get_searches(user)
    for search in searches:
        availability = get_libraries_availability(search.title, search.author)
        if is_free(search, availability):

            book = Book(title=search.title, author=search.author, library=search.library)
            books.append(book)

    mail = Mail(user, books)
    return mail


def add_to_database(searches):
    """ Add a search object to firebase"""
    for search in searches:
        db.collection('search').add(search.change_to_dict())


def get_searches(email=None) -> list[Search]:
    """ Returns all docs from firebase,
    if email is provided returns all searches for this email."""
    if email is None:
        docs = db.collection('searches').stream()
    else:
        docs = db.collection('searches').where(filter=FieldFilter("email", "==", email)).stream()
    searches = []
    for doc in docs:

        # change firebase obj to python dict
        search = doc
        searches.append(search)

    return searches


def remove_search(title: str, author: str, email: str):
    """ Function remove search from database. """
    docs = db.collection('search').where(filter=FieldFilter("title", "==", title)).stream()
    for doc in docs:
        search = doc.to_dict()
        if search['email'] == email and search['author'] == author:
            key = doc.id
            db.collection('searches').document(key).delete()



