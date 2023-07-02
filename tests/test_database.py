from booklovers.database import add_to_registered, remove_email, get_registered_books
from booklovers import parser


def test_add_to_registered():
    book = parser.Book(title="Dziewczynka z zapałkami", author="ola O.", url='wwww.dupa.pl')
    email = 'olkiewicz.alex1234@gmail.com'
    add_to_registered(book, email)


def test_remove_email():
    remove_email(title="Daisy Jones & The Six", author='Reid, Taylor Jenkins',
                 email='olkiewicz.alex1234@gmail.com')


def test_get_registered_books():
    result = get_registered_books(email='olkiewicz.alex1234@gmail.com')
