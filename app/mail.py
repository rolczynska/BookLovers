import yagmail
from datetime import datetime


def send_register_confirmation(title, email):
    mail_from = 'olkiewicz.alex1234@gmail.com'
    mail_to = email
    subject = 'Dostępne książki'
    sender_password = 'epszxtotnzklwwhb'
    yag = yagmail.SMTP(user=mail_from, password=sender_password)
    message = f'You are registered for notification in Raczyński library. When the "{title}" book will be available we will send you an e-mail.'
    cancel_notification = f"If you want to cancel your subscription for this book please click on <a href='http://127.0.0.1:5000/cancel_notify'>THIS LINK.</a>"
    contents = message + cancel_notification
    yag.send(to=mail_to, subject=subject, contents=contents)
    print(f'Mail sent to {email} at {datetime.now() :%d-%m-%Y %H:%M}.')


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