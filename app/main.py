import os
import time
from datetime import datetime
from app import search_web, mail
from tools import json_load, json_dump, HOME


def search_books(path=HOME / "searching_books.json"):
    """Main stages on searching books loop."""
    while True:
        if os.path.isfile(path):
            available_books = check_availability(path)
            send_email_notify(available_books=available_books, path=path)
        print("Already searched for all books. Go to sleep.")
        time.sleep(60 * 60 * 12)


def check_availability(path):
    """Function take a path for searching books and check are they available."""
    available_books = []
    searching_books = json_load(path)
    for title in searching_books.keys():
        url = search_web.get_url(title)
        availability = search_web.check_for_book_status(url)
        if availability:
            available_books.append(title)
    return available_books


def send_email_notify(available_books, path):
    """Function takes titles of available books and send notifications."""
    searching_books = json_load(path)
    for title in available_books:
        emails = searching_books[title]
        for email in emails:
            mail.send_mail(title, email)
            print(f'Book {title} is available. Mail sent to {email} at {datetime.now() :%d-%m-%Y %H:%M}.')
        searching_books.pop(title)
    json_dump(searching_books, path)


if __name__ == '__main__':
    search_books()
