from unittest.mock import patch
from booklovers.connect import get_libraries_availability, get_books_listing
from tests.fixtures.get_library_avability import result


@patch('booklovers.connect.get_page')
def test_get_books_listing(mock_get):
    with open('fixtures/book_listing.html') as file:
        file.read()
    mock_get.return_value = file
    assert get_books_listing(title="dupa") == file


@patch('booklovers.connect.get_books_listing')
def test_get_libraries_availability(mock_get):
    mock_get.return_value = result
    assert get_libraries_availability("Zmierzch", "Meyer, Stephanie") == result

