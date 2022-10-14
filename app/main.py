import json

from app import address, tools, mail
import time


def search_books():
    path = "searching_books.json"
    while True:
        with open(path) as file:
            book_list = json.load(file)
        for title, email in book_list.items():
            # convert it into SINGLE url.
            url = address.get_url(title)
            # checking status for book
            availability = address.check_for_book_status(url)
            # if it is available, send mail and delete from searching_titles.
            if availability:
                mail.send_mail(title, email)
                book_list.pop(title)
        with open("searching_books.json" "w") as file:
            json.dump(book_list, file)
        print("Sleeping...")
        time.sleep(60 * 60 * 12)


if __name__ == '__main__':
    search_books()
