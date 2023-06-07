import re
import threading
from unidecode import unidecode
from flask import Flask, render_template, request, session
from tools import HOME
import search_web
import mail
import main
import book
import forms


app = Flask(__name__)
app.secret_key = "thisissession"

# This is loop for searching books.
searching_books_loop = threading.Thread(target=main.search_books, daemon=True)
searching_books_loop.start()


@app.route("/", methods=["GET", "POST"])
def index():
    book_form = forms.BookForm(csrf_enabled=False)
    if book_form.validate_on_submit():
        title = book_form.title.data
        books = search_web.render_books(title)
        session["books"] = books
        return render_template("display_books.html", books=books)
    return render_template("index.html", book_form=book_form)


@app.route("/availability/<int:book_index>", methods=["GET", "POST"])
def availability(book_index):
    email_form = forms.EmailForm(csrf_enabled=False)
    books = session["books"]
    title = unidecode(books[book_index][1]).strip(" /")
    url = books[book_index][0]
    author = unidecode(books[book_index][2])
    stripped_author = re.sub(r'\([^)]*\)', '', author).strip(" .")
    date = search_web.check_for_book_status(url)
    if email_form.validate_on_submit():
        email = email_form.email.data
        book_id = book.get_id(title=title, author=stripped_author, url=url, path=HOME / "books_index.json")
        if book.add_to_demanded_list(book_id, email, path=HOME / "demanded_books.json"):
            mail.send_register_confirmation(title, email)
        return render_template("email_registered.html")
    return render_template("availability.html", date=date, title=title, author=stripped_author, email_form=email_form)


@app.route("/check_notification", methods=["GET", "POST"])
def check_notification():
    email_form = forms.EmailForm(csrf_enabled=False)
    if email_form.validate_on_submit():
        email = email_form.email.data
        demanded_books = book.get_registered_books(email)
        return render_template("notification_books.html", demanded_books=demanded_books)
    return render_template("check_notification.html", email_form=email_form)


@app.route("/cancel_notify/<title>/<email>")
def cancel_notify(title, email):
    mail.remove_email(title, email)
    return render_template("cancel_subscription.html", title=title)


if __name__ == '__main__':
    app.run(debug=True)
