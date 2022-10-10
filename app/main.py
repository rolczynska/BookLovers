import requests
import yagmail
import time
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime
from app import address


def main():
    """Main stages of program."""
    while True:
        # somehow we need to get the title.
        title = ...
        # and then convert it into SINGLE url.
        urls = address.get_url(title)
        books_status = search_for_status(urls)
        available_books = check_is_it_available(books_status)
        if available_books:
            send_mail(available_books)
        else:
            print("Books you're searching for are unavailable.")
        print("Sleeping...")
        time.sleep(60 * 60 * 12)


def search_for_status(urls: Dict[str, str]) -> Dict[str, list]:
    """Function takes a dict {title: url,...} and return results {title:[status, status]} from the website."""
    results = {}
    for title, url in urls.items():
        result = requests.get(url)
        html = BeautifulSoup(result.text, "html.parser")
        libraries = html.find_all(["tr"], height="15")
        status_for_all_copies = []
        for tag in libraries:
            all_columns = tag.find_all("td")
            first_column = tag.find("td")
            name = first_column.string
            if name == "Wypożyczalnia Al. Marcinkowskiego 23":
                status = all_columns[5].string
                status_for_all_copies.append(status)
        results[title] = status_for_all_copies
    return results


def check_is_it_available(titles_availability: Dict[str, list]) -> List[str]:
    """ Function take a titles and list of statuses and return only available titles."""
    available_books = []
    for title, availability in titles_availability.items():
        if "Na półce" in availability:
            available_books.append(title)
    return available_books


def send_mail(available_books: List[str]):
    """ Function take a list of available books titles and send a mail."""
    mail_from = 'olkiewicz.alex1234@gmail.com'
    mail_to = 'olkiewicz.alex@gmail.com'
    subject = 'Dostępne książki'
    sender_password = 'epszxtotnzklwwhb'
    yag = yagmail.SMTP(user=mail_from, password=sender_password)
    books = ""
    for book in available_books:
        books += book + " "
    contents = 'Dostępne książki:\n' + books
    yag.send(to=mail_to, subject=subject, contents=contents)
    print(f'Mail sent at {datetime.now() :%d-%m-%Y %H:%M}.')


if __name__ == '__main__':
    main()
