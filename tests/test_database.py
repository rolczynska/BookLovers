from booklovers.database import add_to_registered, remove_search, get_registered_books
from booklovers import forms


def test_add_to_registered():
    search = forms.ClientSearch(title="Dziewczynka z zapałkami", author="ola O.",
                                libraries=["marcinkowskiego", "jackowskiego"], email="olkiewiczka@mail.pl")
    add_to_registered(search)


def test_remove_email():
    remove_search(title="Daisy Jones & The Six", author='Reid, Taylor Jenkins',
                  email='olkiewicz.alex1234@gmail.com')


def test_get_registered_books():
    result = get_registered_books(email='olkiewicz.alex1234@gmail.com')
