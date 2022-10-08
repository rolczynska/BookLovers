import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import yagmail
from datetime import datetime
import time

# polskie znaki są jakoś szyfrowane w input wysyłanym do serwera - value='gdzie &#347;piewaj&#261; raki'

urls = {
    "Gdzie śpiewają raki": 'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=PI644T1937881.95392&profile=br-mar&uri=link=3100033~!2696598~!3100021~!3100029&aspect=basic_search&menu=search&ri=1&source=~!bracz&term=Gdzie+śpiewają+raki+%2F&index=ALTITLE',
    "Osiem randek": 'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=PI644T1937881.95392&profile=br-mar&uri=link=3100033~!2710644~!3100021~!3100029&aspect=basic_search&menu=search&ri=3&source=~!bracz&term=Osiem+randek+czyli+Jak+ze+sobą+rozmawiać%2C+żeby+stworzyć+szczęśliwy+związek+%2F&index=ALTITLE',
    "Upór": 'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=PI644T1937881.95392&profile=br-mar&uri=link=3100033~!2547714~!3100021~!3100029&aspect=basic_search&menu=search&ri=5&source=~!bracz&term=Upór+%3A+potęga+pasji+i+wytrwałości+%2F&index=ALTITLE',
    "Pułapki myślenia": 'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=PI644T1937881.95392&profile=br-mar&uri=link=3100033~!2325882~!3100021~!3100029&aspect=basic_search&menu=search&ri=7&source=~!bracz&term=Pułapki+myślenia+%3A+o+myśleniu+szybkim+i+wolnym+%2F&index=ALTITLE',
    }


def main():
    """Main stages of program."""
    while True:
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
