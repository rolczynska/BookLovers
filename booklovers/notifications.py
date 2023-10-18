import time
from booklovers import database
from booklovers.connect import get_libraries_availability
from booklovers.database import get_searches
from booklovers.parser import is_free
from booklovers.forms import Mail, Book


def start_loop():
    """Loop for searching books once per day"""
    while True:
        users = get_users()
        for user in users:
            available_books = get_available_books(user)
            if available_books:
                mail = Mail(user, available_books)
                mail.send()
                remove_searches(user, available_books)

        print("Already searched for all books. Go to sleep.")
        time.sleep(60 * 60 * 12)


def get_users() -> list[str]:
    """ Return all signed users emails """
    users = set()
    searches = get_searches()
    for search in searches:
        users.add(search.email)
    return users


def get_available_books(user: str) -> list[Book]:
    books = []
    searches = get_searches(user)
    for search in searches:
        availability = get_libraries_availability(search.title, search.author)
        if is_free(search, availability):
            book = Book(title=search.title, author=search.author, library=search.library)
            books.append(book)
    return books


def remove_searches(mail, available_books):
    for book in available_books:
        docs = database.db.collection('search').where(filter=database.FieldFilter("title", "==", book.title)).stream()
        for doc in docs:
            search = doc.to_dict()
            if search['email'] == mail and search['author'] == book.author:
                key = doc.id
                database.db.collection('search').document(key).delete()



# def run():
#     """Main stages on demanded books loop. It starts every day."""
#     print("Starting searching")
#     # Checks availability of books registered in database.
#     while True:
#         docs = database.db.collection('books').get()
#         for doc in docs:
#             book = doc.libraries_and_mails_to_dict()
#             url = book['url']
#             availability = parser.get_libraries_availability(url)
#             if availability[0] == 'Na półce':
#                 # Sends notification mail for all followers and delete book from database.
#                 mail.send_mail(title=book['title'], author=book['author'], emails=book['emails'])
#                 book_id = f'{book["author"]} "{book["title"]}"'
#                 database.db.collection('books').document(book_id).delete()
#         print("Already searched for all books. Go to sleep.")
#         time.sleep(60 * 60 * 12)
