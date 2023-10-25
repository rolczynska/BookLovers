from unittest.mock import patch
import pytest
from bs4 import BeautifulSoup

from booklovers.parser import find_books, get_book_info_from_segment, get_books_listing, \
    get_libraries_availability, clean_title, clean_string


@pytest.fixture
def sample_page():
    content = open('fixtures/book_listing.html').read()
    result = BeautifulSoup(content, 'html.parser')
    return result


@pytest.fixture
def sample_segment():
    content = open('fixtures/tr_segment.html').read()
    result = BeautifulSoup(content, 'html.parser')
    return result


@patch('booklovers.parser.get_book_info_from_segment')
def test_find_books(mocked_get_book_info, sample_page):
    mocked_get_book_info.return_value = ("Sample Title", "Sample Author", "url")
    books = find_books(sample_page)
    expected = [('Sample Title', 'Sample Author')]

    assert isinstance(books, list)
    assert books == expected


@patch('booklovers.parser.clean_string', return_value='TEST_CLEAN_AUTHOR')
@patch('booklovers.parser.clean_title', return_value='TEST_CLEAN_TITLE')
def test_get_book_info_from_segment(mocked_clean_name, mocked_clean_title, sample_segment):
    info = get_book_info_from_segment(sample_segment)
    assert isinstance(info, tuple)
    assert len(info) == 3
    assert info == ("TEST_CLEAN_TITLE", "TEST_CLEAN_AUTHOR", "https://TEST_URL.com")


@patch('booklovers.parser.get_page', return_value="sample_page")
def test_get_books_listing(mocked_get_page):
    title = "SampleTitle"
    parsed_page = get_books_listing(title)
    assert parsed_page == "sample_page"


@patch('booklovers.parser.get_urls')
@patch('booklovers.parser.get_page')
def test_get_libraries_availability(mocked_get_page, mocked_get_urls):
    content = open('fixtures/library_rows.html').read()
    sample_page = BeautifulSoup(content, 'html.parser')
    mocked_get_page.return_value = sample_page
    mocked_get_urls.return_value = ["http://sample-url.com"]
    title, author = "SampleTitle", "SampleAuthor"

    result = get_libraries_availability(title, author)

    expected = {'lib1': ['Wypożyczony', '30/10/2023'], 'lib2': ['Na półce', '']}
    assert isinstance(result, dict)
    assert result == expected


def test_clean_string():
    name = "SampleAuthor (SampleInfo)"
    clean_name = clean_string(name)
    assert clean_name == "SampleAuthor"


def test_clean_title():
    title = " SampleTitle /"
    clean_t = clean_title(title)
    assert clean_t == "SampleTitle"
