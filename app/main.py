import json
import os
from app import search_web, tools, mail
import time
from tools import json_load, HOME
from datetime import datetime


# TODO jakoś uprościć funkcje
def search_books():
    path = HOME / "searching_books.json"
    while True:
        if os.path.isfile(path):
            searching_books = json_load(path)
            titles_to_remove = []
            for title, email in searching_books.items():
                # convert it into SINGLE url.
                url = search_web.get_url(title)
                # checking status for book
                availability = search_web.check_for_book_status(url)
                # if it is available, send mail and delete from searching_titles.
                if availability:
                    mail.send_mail(title, email)
                    print(f'Mail sent at {datetime.now() :%d-%m-%Y %H:%M}.')
                    titles_to_remove.append(title)
            tools.delete_from_searching_book_file(titles_to_remove, path)
        print("Already searched for all books. Go to sleep.")
        # jak idzie w aplikacji to się zatrzymuje w tym miejscy na sleeping
        time.sleep(60 * 60 * 12)


if __name__ == '__main__':
    search_books()
