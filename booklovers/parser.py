import re
from dataclasses import dataclass
from typing import List
from bs4 import BeautifulSoup
from unidecode import unidecode


@dataclass
class Book:
    title: str
    author: str
    url: str


def find_books(page: BeautifulSoup) -> List[Book]:
    """This function return a list of lists with info about book like title, author"""
    [table] = page.find_all(cellspacing="1", cellpadding="3")
    trs = table.find_all(height="15")
    books = []
    for tr in trs:
        book = convert_segment_into_book(tr)
        books.append(book)
    return books


def convert_segment_into_book(segment) -> Book:
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
    return Book(title, author, url)


def check_for_book_status(page: BeautifulSoup) -> list:
    """Returns a list with information about the book status."""
    tr_tags_libraries = page.find_all(["tr"], height="15")
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
                date.append(all_columns[6].text)
    return date


def clean_author_name(name: str) -> str:
    return re.sub(r'\([^)]*\)', '', unidecode(name)).strip(" .")


def clean_title(title: str) -> str:
    return unidecode(title).strip(" /")
