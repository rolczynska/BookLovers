from collections import defaultdict
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from dataclasses import dataclass
from configparser import ConfigParser
import yagmail
from pathlib import Path

HOME = Path(__file__).parent
TEMPLATES = HOME / '..' / 'templates'
STATIC = HOME / '..' / 'static'
ASSETS = HOME / '..' / 'static' / 'assets'
MAIN = HOME / '..'


config = ConfigParser()
config.read(MAIN / 'config.ini')
EMAIL_ADDRESS = config['EMAIL']['address']  # 'olkiewicz.alex1234@gmail.com'
EMAIL_PASSWORD = config["EMAIL"]['password']  # epszxtotnzklwwhb


@dataclass
class Search:
    title: str
    author: str
    library: str
    email: str

    def change_to_dict(self):
        data = {
            "title": self.title,
            "author": self.author,
            "library": self.library,
            "email": self.email}
        return data

    @staticmethod
    def from_dict(source):
        title = source['title']
        author = source['author']
        library = source['library']
        email = source['email']
        search = Search(title, author, library, email)
        return search


def create_searches(title: str, author: str, chosen_libraries: list, email: str) -> list[Search]:
    """ Create search object for each library, return list of Search objects"""
    searches = []
    for library in chosen_libraries:
        search = Search(title, author, library, email)
        searches.append(search)
    return searches


@dataclass
class Book:
    title: str
    author: str
    library: str


@dataclass
class Mail:
    email: str
    books: list
    subject: str = 'Dostępne książki'

    def get_books_sorted(self) -> dict[str, list]:
        """Return dictionary with author, title as a key and list of available libraries as value"""
        sorted_books = defaultdict(list)
        for book in self.books:
            key = f"{book.author} {book.title}"
            sorted_books[key].append(book.library)
        return sorted_books

    def send(self) -> dict[str, list]:
        """Send a notification a mail, return dictionary with info about sent books"""
        sorted_books = self.get_books_sorted()
        yag = yagmail.SMTP(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
        with open(TEMPLATES / 'mail_book_available.html', 'r') as file:
            content = file.read()
        logo = yagmail.inline(ASSETS / 'logo_mail.png')
        contents = [logo, content.format(sorted_books=sorted_books)]
        yag.send(to=self.email, subject=self.subject, contents=contents)
        return sorted_books


class BookForm(FlaskForm):
    title = StringField("Tytuł", validators=[DataRequired()])
    submit = SubmitField("Wyszukaj")


class EmailForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),
                                             Email(message='Nieprawidłowy adres email')])
    submit = SubmitField("Zatwierdź")


class SignUpForm(FlaskForm):
    submit = SubmitField("Zapisz się do powiadomień!")
    checkbox = BooleanField(label="library")
