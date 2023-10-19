from collections import defaultdict
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from dataclasses import dataclass
import yagmail
from pathlib import Path
from configparser import ConfigParser
from jinja2 import Environment, FileSystemLoader

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
    libraries: list
    email: str

    def change_to_dict(self):
        data = {
            "title": self.title,
            "author": self.author,
            "libraries": self.libraries,
            "email": self.email}
        return data

    def send_register_confirmation(self):
        """ Sends a registration confirmation email."""
        subject = 'Zapisanie do subskrypcji BookLovers'
        yag = yagmail.SMTP(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)

        # Setup Jinja2 environment and load email template
        env = Environment(loader=FileSystemLoader(str(TEMPLATES)))
        template = env.get_template('mail_content.html')

        # Render the template with the data
        rendered_template = template.render(title=self.title, author=self.author,
                                            chosen_libraries=self.libraries,
                                            email=self.email)
        # Send mail with rendered content
        # TODO pogrubienie tytułu i autora książki w mailu
        yag.send(to=self.email, subject=subject, contents=rendered_template)

    @staticmethod
    def from_dict(source):
        title = source['title']
        author = source['author']
        libraries = source['libraries']
        email = source['email']
        search = Search(title, author, libraries, email)
        return search


@dataclass
class Book:
    title: str
    author: str
    available_libraries: list


@dataclass
class Mail:
    email: str
    books: list
    subject: str = "Dostępne książki"

    def get_books_sorted(self) -> dict[str, list]:
        """Return dictionary with author, title as a key and list of available libraries as value"""
        sorted_books = defaultdict(list)
        for book in self.books:
            key = f'{book.author} "{book.title}"'
            sorted_books[key].append(book.library)
        return sorted_books

    def send(self) -> dict[str, list]:
        """Send a notification a mail, return dictionary with info about sent books"""
        sorted_books = self.get_books_sorted()
        yag = yagmail.SMTP(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)

        # Setup Jinja2 environment and load email template
        env = Environment(loader=FileSystemLoader(str(TEMPLATES)))
        template = env.get_template('mail_book_available.html')

        # Render the template with the data
        rendered_template = template.render(sorted_books=sorted_books)
        #
        contents = rendered_template

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
