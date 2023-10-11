import re
from dataclasses import dataclass
from typing import List, Dict
from bs4 import BeautifulSoup
from unidecode import unidecode
from booklovers import connect


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


def get_urls(page: BeautifulSoup):
    [table] = page.find_all(cellspacing="1", cellpadding="3")
    trs = table.find_all(height="15")
    url_dict = {}
    for tr in trs:
        title, author, url = get_book_info_from_segment(tr)
        if f"{title}, {author}" in url_dict:
            url_dict[f"{title}, {author}"].append(url)
        else:
            url_dict[f"{title}, {author}"] = [url]
    return url_dict


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
            else:
                return_date = None
            result[address] = [status, return_date]
    return result


def clean_author_name(name: str) -> str:
    return re.sub(r'\([^)]*\)', '', unidecode(name)).strip(" .")


def clean_title(title: str) -> str:
    return unidecode(title).strip(" /")
