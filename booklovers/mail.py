import yagmail
from pathlib import Path
from datetime import datetime
from booklovers import database

HOME = Path(__file__).parent
TEMPLATES = HOME / '..' / 'templates'
STATIC = HOME / '..' / 'static'


def send_register_confirmation(title: str, author: str, email: str):
    """ Sends a registration confirmation email."""
    mail_from = 'olkiewicz.alex1234@gmail.com'
    mail_to = email
    subject = 'Dostępne książki'
    sender_password = 'epszxtotnzklwwhb'
    yag = yagmail.SMTP(user=mail_from, password=sender_password)
    with open(TEMPLATES / 'mail_content.html', 'r') as file:
        content = file.read()
        contents = [yagmail.inline(STATIC / 'logo_mail.png'), content.format(title=title,
                                                                             author=author,
                                                                             email=email)]
        yag.send(to=mail_to, subject=subject, contents=contents)
    print(f'Mail sent to {email} at {datetime.now() :%d-%m-%Y %H:%M}.')


def send_mail(title: str, author: str, email: str):
    """ Sends notification email when book is available."""
    mail_from = 'olkiewicz.alex1234@gmail.com'
    mail_to = email
    subject = 'Dostępne książki'
    sender_password = 'epszxtotnzklwwhb'
    yag = yagmail.SMTP(user=mail_from, password=sender_password)
    with open(TEMPLATES / 'mail_book_available.html', 'r') as file:
        content = file.read()
    logo = yagmail.inline(STATIC / 'logo_mail.png')
    contents = [logo, content.format(title=title, author=author)]
    yag.send(to=mail_to, subject=subject, contents=contents)
