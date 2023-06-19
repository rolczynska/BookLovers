import requests
from bs4 import BeautifulSoup


def render_books(title: str) -> list:
    """This function return a list of lists with info about book like title, author"""
    parsed_page = get_book_listing(title)
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


def check_for_book_status(url: str) -> list:
    """Returns a list with information about the book status."""
    parsed_page = get(url)
    tr_tags_libraries = parsed_page.find_all(["tr"], height="15")
    date = []
    for tag in tr_tags_libraries:
        all_columns = tag.find_all("td")
        first_column = all_columns[0]
        name = first_column.string
        if name == "Wypożyczalnia Al. Marcinkowskiego 23":
            status = all_columns[5].string
            if status == "Na półce":
                date.append(status)
            elif status == "Wypożyczony":
                date.append(extract_date(all_columns))
    return date


def extract_date(all_columns: list) -> list:
    """Extracts a date when book should be returned."""
    date = all_columns[6].text
    return date


def get_book_listing(title: str) -> BeautifulSoup:
    """Gets a book listing page. Returns a parsed page by BeautifulSoup."""
    formatted_title = title.replace(" ", "+")
    library = 'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp'
    parameters = f'index=ALTITLE&term={formatted_title}'
    url = f'{library}?{parameters}'
    parsed_page = get(url)
    return parsed_page


def get(url: str, username='spoxb565l6', password='3IpIum3wei9eOaoBl0') -> BeautifulSoup:
    """Gets the website using proxy. Return a parsed page by BeautifulSoup."""
    proxy = f'http://{username}:{password}@pl.smartproxy.com:20001'
    page = requests.get(url, proxies={'http': proxy, 'https': proxy})
    assert page.status_code == 200
    parsed_page = BeautifulSoup(page.text, "html.parser")
    return parsed_page
