import re
from bs4 import BeautifulSoup
from unidecode import unidecode
from booklovers.connect import get_page


def get_book_info_from_segment(segment) -> str:
    """Gets a book info from parsed segment page."""
    a_tabs = segment.find_all('a', class_="smallBoldAnchor")
    url = a_tabs[0].get("href")
    book_info = [url]
    for a in a_tabs:
        single_info = a.text
        book_info.append(single_info)
    if len(book_info) == 6:
        book_info.pop(2)

    url, raw_title, raw_author, *_ = book_info
    title = clean_title(raw_title)
    author = clean_string(raw_author)
    return title, author, url


def find_books(page: BeautifulSoup) -> list[list]:
    """Gets a list with inner lists including title and author from parsed page"""
    [table] = page.find_all(cellspacing="1", cellpadding="3")
    trs = table.find_all(height="15")
    seen = set()
    books = []
    for tr in trs:
        title, author, url = get_book_info_from_segment(tr)
        new_book = f"{title}", f"{author}"
        if new_book not in seen:
            seen.add(new_book)
            books.append(new_book)
    return books


def get_books_listing(title: str) -> BeautifulSoup:
    """Gets a book title. Returns a parsed page by BeautifulSoup with all books listing."""
    formatted_title = title.replace(" ", "+")
    library_url = 'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp'
    parameters = f'index=ALTITLE&term={formatted_title}'
    url = f'{library_url}?{parameters}'
    parsed_page = get_page(url)
    return parsed_page


def get_libraries_availability(title: str, author: str) -> dict:
    """Given a title and author, returns a dictionary detailing the book's status in various
    libraries."""

    ROW_HEIGHT = "15"
    STATUS_INDEX = 5
    RETURN_DATE_INDEX = 6

    result = {}
    urls = get_urls(title, author)

    for url in urls:
        parsed_page = get_page(url)
        library_rows = parsed_page.find_all("tr", height=ROW_HEIGHT)

        for row in library_rows:
            columns = row.find_all("td")
            library_column = columns[0]
            library_name = clean_string(library_column.string)
            status = columns[STATUS_INDEX].string
            return_date = columns[RETURN_DATE_INDEX].text

            result[library_name] = [status, return_date]

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


def clean_string(name: str) -> str:
    return re.sub(r'\([^)]*\)', '', unidecode(name)).strip(" .")


def clean_title(title: str) -> str:
    return unidecode(title).strip(" /")
