import time
from booklovers import database
from booklovers.connect import get_libraries_availability
from booklovers.database import get_searches
from booklovers.forms import Mail, Book, Search


def start_loop():
    """Loop for searching books once per day"""
    while True:
        # get the list of Search objects from database
        searches = get_searches()

        # get unique user emails
        users = get_users(searches)

        for user in users:
            # get available books for each_user
            user_available_books = get_availability(user)
            # if there is any available books for this user send email
            if user_available_books:
                mail = Mail(email=user, books=user_available_books)
                mail.send()
                # remove search for sent books for this user
                remove_searches(mail=user, available_books=user_available_books)
        time.sleep(60 * 60 * 12)


def get_users(searches: list[Search]) -> list[str]:
    """ Return all signed users emails """
    users = set()
    for search in searches:
        users.add(search.email)
    return list(users)


def get_availability(user: str) -> list[Book]:
    """ Take user email and return all available books in those libraries which were signed for
    that emails """
    books = []
    # return book searches for this user
    searches = get_searches(user)
    for search in searches:
        # return data for this book in all libraries
        availability = get_libraries_availability(search.title, search.author)
        # check if is book available in specific library
        available_libraries = get_available_libraries(search, availability)
        if available_libraries:
            book = Book(title=search.title, author=search.author,
                        available_libraries=available_libraries)
            books.append(book)
    return books


def get_available_libraries(search, availability: dict[str, list[str, str]]) -> list[str]:
    """ Check is the book from search available """
    available_libraries = []
    libraries = search.libraries
    for library in libraries:
        status, date = availability.get(library)
        if status == 'Na półce':
            available_libraries.append(library)
    return available_libraries


def remove_searches(mail, available_books):
    for book in available_books:
        docs = database.db.collection('search').where(filter=database.FieldFilter("title", "==", book.title)).stream()
        for doc in docs:
            search = doc.to_dict()
            if search['email'] == mail and search['author'] == book.author:
                key = doc.id
                database.db.collection('search').document(key).delete()

