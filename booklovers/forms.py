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
EMAIL_ADDRESS = config['EMAIL']['address']
EMAIL_PASSWORD = config["EMAIL"]['password']


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

    def to_dict(self):
        data = {
            f"{self.title} {self.author}": f"{self.available_libraries}"
        }
        return data


@dataclass
class Mail:
    email: str
    books: list
    subject: str = "Dostępne książki"

    def get_books_list(self):
        data = []
        for book in self.books:
            book.to_dict()
            data.append(book)
        return data

    def send(self):
        """Send a notification a mail."""
        yag = yagmail.SMTP(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)

        # Setup Jinja2 environment and load email template
        env = Environment(loader=FileSystemLoader(str(TEMPLATES)))
        template = env.get_template('mail_book_available.html')

        # Render the template with the data
        contents = template.render(books=self.books)

        yag.send(to=self.email, subject=self.subject, contents=contents)


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
