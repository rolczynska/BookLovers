import requests
from bs4 import BeautifulSoup


def render_books(title: str) -> list:
    """This function return a list of lists with info about book like title, author"""
    replaced_title = title.replace(" ", "+")
    url_formula = f'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?index=ALTITLE&term={replaced_title}'
    page = requests.get(url_formula)
    parsed_page = BeautifulSoup(page.text, "html.parser")
    table = parsed_page.find_all(cellspacing="1", cellpadding="3")[0]
    trs = table.find_all(height="15")
    books = []
    for tr in trs:
        a_tabs = tr.find_all('a', class_="smallBoldAnchor")
        book_url = a_tabs[0].get("href")
        book_info = [book_url]
        for a in a_tabs:
            single_info = a.text
            book_info.append(single_info)
        if len(book_info) == 6:
            book_info.pop(2)
        books.append(book_info)
    return books


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


