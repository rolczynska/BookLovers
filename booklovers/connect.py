from typing import Dict

import requests
from bs4 import BeautifulSoup

from booklovers.parser import get_book_info_from_segment


def get_books_listing(title: str) -> BeautifulSoup:
    """Gets a book listing page. Returns a parsed page by BeautifulSoup."""
    formatted_title = title.replace(" ", "+")
    library = 'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp'
    parameters = f'index=ALTITLE&term={formatted_title}'
    url = f'{library}?{parameters}'
    parsed_page = get_page(url)
    return parsed_page


def get_page(url: str, username='spoxb565l6', password='3IpIum3wei9eOaoBl0') -> BeautifulSoup:
    """Gets the website using proxy. Return a parsed page by BeautifulSoup."""
    proxy = f'http://{username}:{password}@pl.smartproxy.com:20001'
    page = requests.get(url, proxies={'http': proxy, 'https': proxy})
    assert page.status_code == 200
    parsed_page = BeautifulSoup(page.text, "html.parser")
    return parsed_page


def get_libraries_availability(title: str, author: str) -> Dict:
    """Returns a list with information about the book status in every library."""
    result = {}
    urls = get_urls(title, author)
    for url in urls:
        parsed_page = get_page(url)
        tr_tags_libraries = parsed_page.find_all(["tr"], height="15")
        for tr in tr_tags_libraries:
            all_columns = tr.find_all("td")
            first_column = all_columns[0]
            address = first_column.string
            status = all_columns[5].string
            return_date = all_columns[6].text
            result[address] = [status, return_date]
    return result


def get_urls(title: str, author: str) -> list[str]:
    """Retrieve all possible links under which the book can be found."""
    page = get_books_listing(title)
    [table] = page.find_all(cellspacing="1", cellpadding="3")
    trs = table.find_all(height="15")
    urls = []
    for tr in trs:
        search_title, search_author, url = get_book_info_from_segment(tr)
        if title == search_title and author == search_author:
            urls.append(url)
    return urls

