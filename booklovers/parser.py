import re
from typing import List, Dict
from bs4 import BeautifulSoup
from unidecode import unidecode
from booklovers import connect, forms


def find_books(page: BeautifulSoup) -> List[List]:
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


def get_urls(title, author):
    page = connect.get_book_listing(title)
    [table] = page.find_all(cellspacing="1", cellpadding="3")
    trs = table.find_all(height="15")
    urls = []
    for tr in trs:
        search_title, search_author, url = get_book_info_from_segment(tr)
        if title == search_title and author == search_author:
            urls.append(url)
    return urls


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
    author = clean_author_name(raw_author)
    return title, author, url


def get_libraries_availability(urls: List[str]) -> Dict:
    """Returns a list with information about the book status."""
    result = {}
    for url in urls:
        parsed_page = connect.get(url)
        tr_tags_libraries = parsed_page.find_all(["tr"], height="15")
        for tr in tr_tags_libraries:
            all_columns = tr.find_all("td")
            first_column = all_columns[0]
            address = first_column.string
            status = all_columns[5].string
            if status == "Wypożyczony":
                return_date = all_columns[6].text
                result[address] = [status, return_date]
            else:
                result[address] = [status]
    return result


def get_libraries_for_sign_up(libraries_availability) -> Dict:
    new_dict = {}
    for library, info in libraries_availability.items():
        if info[0] == "Wypożyczony":
            new_dict[library] = info
    return new_dict


def get_search_obj(title, author, chosen_libraries, email):
    libraries_with_emails = {library: [email] for library in chosen_libraries}
    return forms.Search(title, author, libraries_with_emails)


def clean_author_name(name: str) -> str:
    return re.sub(r'\([^)]*\)', '', unidecode(name)).strip(" .")


def clean_title(title: str) -> str:
    return unidecode(title).strip(" /")
