import requests
from bs4 import BeautifulSoup


def get_title_author_url(title: str):
    """ Function take a title from user and search for this book in library.
     Return a title, author and the url."""
    replaced_title = title.replace(" ", "+")
    url_formula = f'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?index=ALTITLE&term={replaced_title}'
    page = requests.get(url_formula)
    parsed_page = BeautifulSoup(page.text, "html.parser")
    tags = parsed_page.find_all(class_="smallBoldAnchor")
    web_title = tags[0].text
    web_author = tags[1].text
    url = tags[0].get("href")
    return web_title, web_author, url


def check_for_book_status(url) -> bool:
    """ Function take a url and search for book status in library on Al. Marcinkowskiego 23. Return Boolean"""
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


def get_url(title):
    replaced_title = title.replace(" ", "+")
    url_formula = f'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?index=ALTITLE&term={replaced_title}'
    page = requests.get(url_formula)
    parsed_page = BeautifulSoup(page.text, "html.parser")
    tags = parsed_page.find_all(class_="smallBoldAnchor")
    url = tags[0].get("href")
    return url


