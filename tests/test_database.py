from booklovers import database
from booklovers import parser


def test_add_to_registered():
    book = parser.Book(title="Dziewczynka z zapałkami", author="ola O.", url='wwww.dupa.pl')
    email = 'olkiewicz.alex1234@gmail.com'
    database.add_to_registered(book, email)
