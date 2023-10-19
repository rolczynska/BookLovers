import re
from typing import List
from bs4 import BeautifulSoup
from unidecode import unidecode


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


def clean_author_name(name: str) -> str:
    return re.sub(r'\([^)]*\)', '', unidecode(name)).strip(" .")


def clean_title(title: str) -> str:
    return unidecode(title).strip(" /")
