import re
import threading
from unidecode import unidecode
from flask import Flask, render_template, session
from booklovers.tools import HOME
from booklovers import search
from booklovers import mail
from booklovers import main
from booklovers import book
from booklovers import forms

# We create a Flask app.
app = Flask(__name__)

# This is a loop for searching demanded books.
demanded_books_loop = threading.Thread(target=main.search_books, daemon=True)
demanded_books_loop.start()


@app.route("/", methods=["GET", "POST"])
def index():
    # Search for books.
    book_form = forms.BookForm(csrf_enabled=False)

    # If a form is validated, we search for books and render them.
    if book_form.validate_on_submit():
        title = book_form.title.data

        # We get books from search module and save them in session.
        books = search.get_books(title)
        session["books"] = books

        return render_template("display_books.html", books=books)
    return render_template("index.html", book_form=book_form)


@app.route("/availability/<int:book_index>", methods=["GET", "POST"])
def availability(book_index):
    # Checks the availability of a book.
    email_form = forms.EmailForm(csrf_enabled=False)
    chosen_book = session["books"][book_index]
    url, raw_title, raw_author = chosen_book

    # We get title, author and date of a book.
    title = unidecode(raw_title).strip(" /")
    author = re.sub(r'\([^)]*\)', '', unidecode(raw_author)).strip(" .")
    date = search.check_for_book_status(url)
    params = {"title": title, "author": author, "url": url, "date": date}

    # If a form is validated, we add a book to demanded list and render a page.
    if email_form.validate_on_submit():
        email = email_form.email.data
        book_id = book.get_id(**params, path=HOME / "books_index.json")
        if book.add_to_demanded_list(book_id, email, path=HOME / "demanded_books.json"):
            mail.send_register_confirmation(title, email)

        return render_template("email_registered.html")
    return render_template("availability.html", **params, email_form=email_form)


@app.route("/check_notification", methods=["GET", "POST"])
def check_notification():
    # Checks user book notifications.
    email_form = forms.EmailForm(csrf_enabled=False)
    if email_form.validate_on_submit():
        email = email_form.email.data
        demanded_books = book.get_registered_books(email)
        return render_template("notification_books.html", demanded_books=demanded_books)
    return render_template("check_notification.html", email_form=email_form)


@app.route("/cancel_notify/<title>/<email>")
def cancel_notify(title, email):
    # Cancels user book notifications.
    mail.remove_email(title, email)
    return render_template("cancel_subscription.html", title=title)


if __name__ == '__main__':
    app.run(debug=True)
