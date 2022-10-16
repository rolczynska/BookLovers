import requests
from bs4 import BeautifulSoup
from datetime import datetime
# https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?index=ALTITLE&term=siedem+żyć --> pierwszy link
# https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=166B5852R74W9.199857&amp;profile=br-mar&amp;uri=link=3100033~!2651526~!3100021~!3100029&amp;aspect=basic_search&amp;menu=search&amp;ri=1&amp;source=~!bracz&amp;term=365+dni+%2F&amp;index=ALTITLE


# TODO sprawdzić czy to na pewno ten tytuł i autor, sprawdzić czy nie ma dwóch pozycji tego samego tytułu (inne wydanie)
def get_url(title: str):
    """ Function take a title and return an url where information about book status is display."""
    replaced_title = title.replace(" ", "+")
    url_formula = f'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?index=ALTITLE&term={replaced_title}'
    page = requests.get(url_formula)
    parsed_page = BeautifulSoup(page.text, "html.parser")
    tags = parsed_page.find(class_="smallBoldAnchor", href=True)
    web_title = tags.text
    if web_title == title:
        url = tags.get("href")
        return url
    return False


# TODO Co jeśli nie ma książki ? - zaimplementuj odpowiedź
def check_for_book_status(url) -> bool:
    """ Function will take a url and check for book status. Return Boolean"""
    page = requests.get(url)
    parsed_page = BeautifulSoup(page.text, "html.parser")
    tr_tags_libraries = parsed_page.find_all(["tr"], height="15")
    book_status = []
    for tag in tr_tags_libraries:
        all_columns = tag.find_all("td")
        first_column = tag.find("td")
        name = first_column.string
        if name == "Wypożyczalnia Al. Marcinkowskiego 23":
            status = all_columns[5].string
            book_status.append(status)
    if "Na półce" in book_status:
        return True
    else:
        return False
