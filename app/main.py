from app import address, tools, mail
import time


def first_check():
    """ Stages when user enter a title in applicati"""
    # program ma się odpalać gdy ktoś wyśle zapytanie za pomocą formularza - przycisk submit
    # we get the title.
    title = ...
    while title:
        # convert it into SINGLE url.
        url = address.get_url(title)
        # checking status for book
        availability = address.check_for_book_status(url)
        if not availability:
            # if it is not availabile ask about mail
            email = ...
            # sprawdzamy czy tytuł z tym mailem jest dodany do listy sprawdzającej
            if not tools.is_already_registered(title, email):
                # jeśli nie jest zarejestrwana to wysyłamy potwierdzenie i dodajemy tytuł i email do listy
                mail.send_register_confirmation(title, email)
                tools.add_to_list(title, email)
            else:
                return "You are already registered for that book."
        return "Your book is already available!"


def searching_books():
    while True:
        for title, email in tools.searching_titles.items():
            # convert it into SINGLE url.
            url = address.get_url(title)
            # checking status for book
            availability = address.check_for_book_status(url)
            # if it is available, send mail and delete from searching_titles.
            if availability:
                mail.send_mail(title, email)
                tools.searching_titles.pop(title)
        print("Sleeping...")
        time.sleep(60 * 60 * 12)


if __name__ == '__main__':
    searching_books()
