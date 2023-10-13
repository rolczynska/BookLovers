import yagmail
from pathlib import Path
from datetime import datetime

HOME = Path(__file__).parent
TEMPLATES = HOME / '..' / 'templates'
STATIC = HOME / '..' / 'static'
ASSETS = HOME / '..' / 'static' / 'assets'


def send_register_confirmation(title: str, author: str, chosen_libraries: list, email: str):
    """ Sends a registration confirmation email."""
    mail_from = 'olkiewicz.alex1234@gmail.com'
    mail_to = email
    subject = 'Dostępne książki'
    sender_password = 'epszxtotnzklwwhb'
    yag = yagmail.SMTP(user=mail_from, password=sender_password)
    with open(TEMPLATES / 'mail_content.html', 'r') as file:
        content = file.read()
        contents = [yagmail.inline(ASSETS / 'logo_mail.png'),
                    content.format(title=title, author=author, chosen_libraries=chosen_libraries,
                                   email=email)]
        yag.send(to=mail_to, subject=subject, contents=contents)
    print(f'Mail sent to {email} at {datetime.now() :%d-%m-%Y %H:%M}.')


def send_mail(title: str, author: str, emails: list):
    """ Sends notifications when book is available."""
    mail_from = 'olkiewicz.alex1234@gmail.com'
    subject = 'Dostępne książki'
    sender_password = 'epszxtotnzklwwhb'
    yag = yagmail.SMTP(user=mail_from, password=sender_password)
    with open(TEMPLATES / 'mail_book_available.html', 'r') as file:
        content = file.read()
    logo = yagmail.inline(ASSETS / 'logo_mail.png')
    contents = [logo, content.format(title=title, author=author)]
    for email in emails:
        yag.send(to=email, subject=subject, contents=contents)
