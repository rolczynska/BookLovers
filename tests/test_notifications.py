from booklovers.notifications import get_users, get_availability, get_available_libraries
from booklovers.forms import Search, Book
from unittest.mock import patch


def test_get_users():
    search1 = Search("Sample Title", "Sample Author", ["lib1", "lib2"], "sample@mail.com")
    search2 = Search("Sample Title", "Sample Author", ["lib1", "lib2"], "sample@mail.com")
    search3 = Search("Sample Title", "Sample Author", ["lib1", "lib2"], "anothersample@mail.com")
    search4 = Search("Another Sample Title", "Sample Author", ["lib1", "lib2"],
                     "anothersample@mail.com")
    searches = [search1, search2, search3, search4]
    result = get_users(searches)

    assert len(result) == 2
    assert len(result) == len(set(result))


class TestAvailableLibraries:
    def test_get_available_lib_two_available(self):
        search = Search("Sample Title", "Sample Author", ["lib1", "lib2"], "sample@mail.com")
        availability = {"lib1": ["Na półce", " "], "lib2": ["Na półce", " "]}

        result = get_available_libraries(search, availability)
        expected = ["lib1", "lib2"]
        assert result == expected

    def test_get_available_lib_one_available(self):
        search = Search("Sample Title", "Sample Author", ["lib1", "lib2"], "sample@mail.com")
        availability = {"lib1": ["Na półce", " "], "lib2": ["Wypożyczony", "25/04/2023"]}

        result = get_available_libraries(search, availability)
        expected = ["lib1"]
        assert result == expected

    def test_get_available_lib_not_available(self):
        search = Search("Sample Title", "Sample Author", ["lib2"], "sample@mail.com")
        availability = {"lib1": ["Na półce", " "], "lib2": ["Wypożyczony", "25/04/2023"]}

        result = get_available_libraries(search, availability)
        expected = []
        assert result == expected


@patch('booklovers.notifications.get_searches')
@patch('booklovers.notifications.get_libraries_availability')
@patch('booklovers.notifications.get_available_libraries')
def test_get_availability(mocked_get_available_libraries, mocked_get_libraries_availability,
                          mocked_get_searches):
    mocked_get_searches.return_value = [
        Search("Sample Title", "Sample Author", ["lib1", "lib2"], "sample@mail.com"),
        Search("Another Sample Title", "Sample Author", ["lib2"], "sample@mail.com")]
    mocked_get_libraries_availability.return_value = {"lib1": ["Na półce", " "],
                                                      "lib2": ["Na półce", " "]}
    mocked_get_available_libraries.return_value = ["lib1", "lib2"]

    result = get_availability("sample@mail.com")
    expected = [
        Book(title='Sample Title', author='Sample Author', available_libraries=['lib1', 'lib2']),
        Book(title='Another Sample Title', author='Sample Author',
             available_libraries=['lib1', 'lib2'])]
    assert result == expected
