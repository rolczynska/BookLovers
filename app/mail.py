import yagmail
from datetime import datetime


def send_register_confirmation(title, email):
    pass


def send_mail(title, email):
    """ Function will send email when book will be available."""
    mail_from = 'olkiewicz.alex1234@gmail.com'
    mail_to = email
    subject = 'Dostępne książki'
    sender_password = 'epszxtotnzklwwhb'
    yag = yagmail.SMTP(user=mail_from, password=sender_password)
    contents = f'Huuray! "{title}" is already available in Raczyński library. Go and borrow it!'
    yag.send(to=mail_to, subject=subject, contents=contents)
    print(f'Mail sent to {email} at {datetime.now() :%d-%m-%Y %H:%M}.')