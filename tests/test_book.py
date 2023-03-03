import book
import tools
# TODO zmień, żeby wszystkei testy były wykonywane na pliku testowym path i potem żeby był on kasowany


def test_is_in_book_ids():
    result = book.is_in_books_ids(title="Zmierzch", author="Meyer, Stephanie", path=tools.HOME/"books_id.json")
    assert result == True

    result = book.is_in_books_ids(title="Gdzie spiewaja raki", author="Meyer, Stephanie", path=tools.HOME/"books_id.json")
    assert result == False


def test_get_id():
    book_id = book.get_id(title="Zmierzch", author="Meyer, Stephanie", path=tools.HOME/"books_id.json")
    assert book_id == "2"


def test_get_next_id():
    books_ids = tools.json_load(path=tools.HOME/"books_id.json")
    book_id = book.get_next_id(books_ids)
    assert book_id == "3"


def test_add_to_books_ids():
    id = book.add_to_books_ids(title="Gdzie śpiewają raki", author="Rafal, Rolczynski", url="https:blabla", path="fixtures/books_id.json")
    content = tools.json_load(path="fixtures/books_id.json")
    assert content[id]["title"] == "Gdzie śpiewają raki"


def test_is_already_registered():
    pass


def test_get_books_from_ids():
    books = book.get_books_from_ids(some_books_id=["1"])
    assert ["Zmierzch", "Kupka, Stephanie"] in books
     
