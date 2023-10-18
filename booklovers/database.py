from google.cloud.firestore_v1 import FieldFilter

from booklovers.forms import Search, MAIN
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate(MAIN / "ServiceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def add_to_database(searches):
    """ Add a search object to firebase"""
    for search in searches:
        doc_id = create_unique_id(search.author, search.title, search.library, search.email)
        db.collection('search').document(doc_id).set(search.change_to_dict())


def get_searches(email=None) -> list[Search]:
    """ Returns all docs from firebase,
    if email is provided returns all searches for this email."""
    if email is None:
        docs = db.collection('search').stream()
    else:
        docs = db.collection('search').where(filter=FieldFilter("email", "==", email)).stream()
    searches = []
    for doc in docs:

        # change firebase obj to python dict
        search = doc.to_dict()
        search_obj = Search.from_dict(search)
        searches.append(search_obj)

    return searches


def remove_search(title: str, author: str, email: str):
    """ Function remove search from database. """
    docs = db.collection('search').where(filter=FieldFilter("title", "==", title)).stream()
    for doc in docs:
        search = doc.to_dict()
        if search['email'] == email and search['author'] == author:
            db.collection('search').document(doc.id).delete()


def create_unique_id(*strings):
    id = ""
    for string in strings:
        id += (string[:2] + str(len(string)) + string[-2:])
    return id
