from booklovers import mail


def test_send_mail():
    mail.send_mail(title='Tytuł', author='Author',
                   emails=['olkiewicz.alex1234@gmail.com', 'olkiewicz.alex@gmail.com'])
