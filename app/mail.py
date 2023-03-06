import os

import yagmail
from datetime import datetime
from tools import HOME, json_load, json_dump

TEMPLATES = HOME / '..' / 'templates'
STATIC = HOME / '..' / 'static'


def send_register_confirmation(title, email):
    """Function send a confirmation after registration for notification."""
    mail_from = 'olkiewicz.alex1234@gmail.com'
    mail_to = email
    subject = 'Dostępne książki'
    sender_password = 'epszxtotnzklwwhb'
    yag = yagmail.SMTP(user=mail_from, password=sender_password)
    with open(TEMPLATES / 'mail_content.html', 'r') as file:
        content = file.read()
        contents = [yagmail.inline(STATIC / 'logo_mail.png'), content.format(title=title, email=email)]
        yag.send(to=mail_to, subject=subject, contents=contents)
    print(f'Mail sent to {email} at {datetime.now() :%d-%m-%Y %H:%M}.')


def send_mail(title, author, email):
    """ Function will send email when book will be available."""
    mail_from = 'olkiewicz.alex1234@gmail.com'
    mail_to = email
    subject = 'Dostępne książki'
    sender_password = 'epszxtotnzklwwhb'
    yag = yagmail.SMTP(user=mail_from, password=sender_password)
    with open(TEMPLATES / 'mail_book_available.html', 'r') as file:
        content = file.read()
    contents = content.format(title=title, author=author)
    yag.send(to=mail_to, subject=subject, contents=contents)
    print(f'Mail sent to {email} at {datetime.now() :%d-%m-%Y %H:%M}.')


def remove_email(book_id, email, path=HOME / 'searching_books.json'):
    """Function take title and email and remove book from notification list. """
    if os.path.isfile(path):
        searching_books = json_load(path)
        try:
            searching_books[book_id].remove(email)
            if len(searching_books[book_id]) == 0:
                searching_books.pop(book_id)
        except (KeyError, ValueError):
            json_dump(searching_books, path)
    else:
        searching_books = {}
    json_dump(searching_books, path)