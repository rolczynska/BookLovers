import requests
from bs4 import BeautifulSoup
# https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?index=ALTITLE&term=365+dni --> pierwszy link
# https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=166B5852R74W9.199857&amp;profile=br-mar&amp;uri=link=3100033~!2651526~!3100021~!3100029&amp;aspect=basic_search&amp;menu=search&amp;ri=1&amp;source=~!bracz&amp;term=365+dni+%2F&amp;index=ALTITLE


def get_url(title: str) -> str:
    """ Function take a title and return a url where information about book status is display."""
    replaced_title = title.replace(" ", "+")
    url_formula = f'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?index=ALTITLE&term={replaced_title}'
    page = requests.get(url_formula)
    parsed_page = BeautifulSoup(page.text, "html.parser")
    tags = parsed_page.find(class_="smallBoldAnchor", href=True)
    url_with_book_status = tags.get("href")
    return url_with_book_status


def search_for_book_status(url):
    pass


def send_mail(title, email):
    pass

