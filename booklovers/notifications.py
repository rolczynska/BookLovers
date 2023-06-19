import os
import time
from datetime import datetime
from booklovers import mail


def run():
    """Main stages on demanded books loop. It starts every day."""
    print("Starting searching")
    while True:
        if os.path.isfile(path):
            available_books = check_availability(path)
            send_email_notify(available_books=available_books, path=path)
            print("Already searched for all books. Go to sleep.")
            time.sleep(60 * 60 * 12)
        else:
            var = {}
            json_dump(var, path)


def check_availability(path=HOME / "demanded_books.json") -> list:
    """Function checks, are the demanded books available. Return list of available_books."""
    available_books = []
    demanded_books = json_load(path)
    if os.path.isfile(path=HOME / "books_index.json"):
        books_index = json_load(path=HOME / "books_index.json")
        for book_id in demanded_books:
            url = booklovers.connect.get("url")
            availability = search.check_for_book_status(url)
            if 'Na półce' in availability:
                title = booklovers.connect.get("title")
                author = booklovers.connect.get("author")
                available_books.append([book_id, title, author])
    print("Exit check_availability")
    return available_books


def send_email_notify(available_books: list, path: str):
    """Function takes list of available books contains book_id, title and author and send notify."""
    demanded_books = json_load(path)
    for book in available_books:
        book_id = book[0]
        title = book[1]
        author = book[2]
        emails = booklovers.connect.get(book_id)
        for email in emails:
            mail.send_mail(title, author, email)
            print(f'Book {title} is available. Mail sent to {email} at '
                  f'{datetime.now() :%d-%m-%Y %H:%M}.')
        demanded_books.pop(book_id)
    json_dump(demanded_books, path)
    print("Exit send_email_notify")
