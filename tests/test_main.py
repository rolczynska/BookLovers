import os

import book
import main
import tools
TESTS = tools.HOME / ".." / "fixtures"


def test_search_books():
    path = TESTS / "searching_books.json"
    book.add_to_demanded_list("365 dni", "olkiewicz.alex1234@gmail.com", path)
    main.search_books(path=path)
    os.remove(path)


def test_check_availability():
    path = TESTS / "searching_books.json"
    book.add_to_demanded_list("365 dni", "olkiewicz.alex1234@gmail.com", path)
    book.add_to_demanded_list("365 dni", "olkiewicz.alex1234@gmail.com", path)
    book.add_to_demanded_list("gdzie śpiewają raki", "olkiewicz.alex1234@gmail.com", path)
    availability = main.check_availability(path)
    assert availability == ["365 dni"]
    os.remove(path)


def test_send_email_notify():
    path = TESTS / "searching_books.json"
    book.add_to_demanded_list("365 dni", "olkiewicz.alex1234@gmail.com", path)
    book.add_to_demanded_list("365 dni", "olkiewicz.alex1234@gmail.com", path)
    book.add_to_demanded_list("Kobieta w walizce", "olkiewicz.alex1234@gmail.com", path)
    main.send_email_notify(available_books=["365 dni"], path=path)
    os.remove(path)
