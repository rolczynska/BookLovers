
import yagmail
from datetime import datetime
from app_directory.tools import HOME, json_load, json_dump
from app_directory.book import get_id

TEMPLATES = HOME / '..' / 'templates'
STATIC = HOME / '..' / 'static'


def send_register_confirmation(title: str, email: str):
    """ Sends a registration confirmation email."""
    mail_from = 'olkiewicz.alex1234@gmail.com'
    mail_to = email
    subject = 'Dostępne książki'
    sender_password = 'epszxtotnzklwwhb'
    yag = yagmail.SMTP(user=mail_from, password=sender_password)
    with open(TEMPLATES / 'mail_content.html', 'r') as file:
        content = file.read()
        contents = [yagmail.inline(STATIC / 'logo_mail.png'), content.format(title=title,
                                                                             email=email)]
        yag.send(to=mail_to, subject=subject, contents=contents)
    print(f'Mail sent to {email} at {datetime.now() :%d-%m-%Y %H:%M}.')


def send_mail(title: str, author: str, email: str):
    """ Sends notification email when book will be available."""
    mail_from = 'olkiewicz.alex1234@gmail.com'
    mail_to = email
    subject = 'Dostępne książki'
    sender_password = 'epszxtotnzklwwhb'
    yag = yagmail.SMTP(user=mail_from, password=sender_password)
    with open(TEMPLATES / 'mail_book_available.html', 'r') as file:
        content = file.read()
    contents = [yagmail.inline(STATIC / 'logo_mail.png'), content.format(title=title,
                                                                         author=author)]
    yag.send(to=mail_to, subject=subject, contents=contents)


def remove_email(title: str, email: str):
    """Function remove book from notification list. """
    book_id = get_id(title, path=HOME / "books_index.json")
    demanded_books = json_load(path=HOME / "demanded_books.json")
    if book_id in demanded_books:
        demanded_books[book_id].remove(email)
        if len(demanded_books[book_id]) == 0:
            demanded_books.pop(book_id)
    json_dump(demanded_books, path=HOME / "demanded_books.json")
