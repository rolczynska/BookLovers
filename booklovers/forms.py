from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from dataclasses import dataclass
# from booklovers.database import db
import yagmail
from pathlib import Path


HOME = Path(__file__).parent
TEMPLATES = HOME / '..' / 'templates'
STATIC = HOME / '..' / 'static'
ASSETS = HOME / '..' / 'static' / 'assets'


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

    def get_books_sorted(self) -> dict[str, list]:
        """Return dictionary with author, title as a key and list of available libraries as value"""
        sorted_books = {}
        for book in self.books:
            key = f"{book.author} {book.title}"
            if key in sorted_books:
                sorted_books[key].append(book.library)
            else:
                sorted_books[key] = [book.library]
        return sorted_books

    def send(self) -> dict[str, list]:
        """Send a notification a mail, return dictionary with info about sent books"""
        sorted_books = self.get_books_sorted()
        mail_from = 'olkiewicz.alex1234@gmail.com'
        subject = 'Dostępne książki'
        sender_password = 'epszxtotnzklwwhb'
        yag = yagmail.SMTP(user=mail_from, password=sender_password)
        with open(TEMPLATES / 'mail_book_available.html', 'r') as file:
            content = file.read()
        logo = yagmail.inline(ASSETS / 'logo_mail.png')
        contents = [logo, content.format(sorted_books=sorted_books)]
        yag.send(to=self.email, subject=subject, contents=contents)
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
