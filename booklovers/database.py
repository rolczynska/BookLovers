from google.cloud.firestore_v1 import FieldFilter

from booklovers.forms import Search, MAIN
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate(MAIN / "ServiceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def add_to_database(search):
    """ Add a search object to firebase"""
    doc_id = create_unique_id(search.author, search.title, search.email)
    db.collection('search').document(doc_id).set(search.change_to_dict(), merge=True)


def get_searches(email=None) -> list[Search]:
    """ Returns all searches from firebase,
    if email is provided returns all searches with this email."""
    if email is None:
        docs = db.collection('search').stream()
    else:
        docs = db.collection('search').where(filter=FieldFilter("email", "==", email)).stream()
    searches = []
    for doc in docs:

        # change firebase obj to python dict
        search = doc.to_dict()

        # change from dict to Search obj
        search_obj = Search.from_dict(search)
        searches.append(search_obj)

    return searches


def remove_search(title: str, author: str, email: str):
    """ Function to remove search from database. """
    docs = db.collection('search').where(filter=FieldFilter("title", "==", title)).stream()
    for doc in docs:
        search = doc.to_dict()
        if search['email'] == email and search['author'] == author:
            db.collection('search').document(doc.id).delete()


def create_unique_id(*strings: str) -> str:
    """ Function create unique id for each unique search. """
    id = ""
    for string in strings:
        id += (string[:2] + str(len(string)) + string[-2:])
    return id
