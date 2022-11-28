import yagmail
from datetime import datetime
from tools import HOME
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


def send_mail(title, email):
    """ Function will send email when book will be available."""
    mail_from = 'olkiewicz.alex1234@gmail.com'
    mail_to = email
    subject = 'Dostępne książki'
    sender_password = 'epszxtotnzklwwhb'
    yag = yagmail.SMTP(user=mail_from, password=sender_password)
    with open(TEMPLATES / 'mail_book_available.html', 'r') as file:
        content = file.read()
    contents = content.format(title=title)
    yag.send(to=mail_to, subject=subject, contents=contents)
    print(f'Mail sent to {email} at {datetime.now() :%d-%m-%Y %H:%M}.')
