import json
import os
from app import address, tools, mail
import time
from tools import json_load, HOME


def search_books():
    path = HOME / "searching_books.json"
    while True:
        if os.path.isfile(path):
            book_list = json_load(path)
            titles_to_remove = []
            for title, email in book_list.items():
                # convert it into SINGLE url.
                url = address.get_url(title)
                # checking status for book
                availability = address.check_for_book_status(url)
                # if it is available, send mail and delete from searching_titles.
                if availability:
                    mail.send_mail(title, email)
                    titles_to_remove.append(title)
            tools.delete_from_searching_book_file(titles_to_remove, path)
        print("Sleeping...")
        time.sleep(60 * 60 * 12)


if __name__ == '__main__':
    search_books()
