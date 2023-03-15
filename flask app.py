import os
import re
import threading
from unidecode import unidecode
from flask import Flask, render_template, request, session, redirect, url_for
from tools import HOME
import search_web
import mail
import main
import book
import forms


app = Flask(__name__)
app.secret_key = "thisissession"

''' This is loop for searching books.'''
searching_books_loop = threading.Thread(target=main.search_books, daemon=True)
#searching_books_loop.start()


@app.route("/", methods=["GET", "POST"])
def index():
    book_form = forms.BookForm(csrf_enabled=False)
    if book_form.validate_on_submit():
        title = book_form.title.data
        books = search_web.render_books(title)
        session["books"] = books
        return render_template("display_books.html", books=books)
    return render_template("index.html", book_form=book_form)


@app.route("/availability/<book_index>")
def availability(book_index):
    book_index = int(book_index)
    books = session["books"]
    print(books)
    url = books[book_index][0]
    session["url"] = url
    title = unidecode(books[book_index][1]).strip(" /")
    session["title"] = title
    author = unidecode(books[book_index][2])
    stripped_author = re.sub(r'\([^)]*\)', '', author).strip(" .")
    session["author"] = stripped_author
    date = search_web.check_for_book_status(url)
    print(url)
    print(date)
    if date == "Na półce":
        return render_template("book_available.html", title=title, author=stripped_author)
    elif date == "":
        return render_template("no_book.html")
    else:
        return render_template("enter_email.html", date=date)


@app.route("/enter_email", methods=["GET", "POST"])
def enter_email():
    if request.method == "POST":
        title = session["title"]
        url = session["url"]
        author = session["author"]
        email = request.form.get("email")
        if book.is_in_books_index(title, author, path=HOME / "books_index.json"):
            book_id = book.get_id(title, author, path=HOME / "books_index.json")
            if book.is_mail_registered(book_id, email):
                return render_template("already_registered.html")
        else:
            book_id = book.add_to_books_index(title, author, url, path=HOME / "books_index.json")
        book.add_to_searching_list(book_id, email, path=HOME / "searching_books.json")
        mail.send_register_confirmation(title, email)
        return render_template("email_registered.html")
    else:
        return redirect(url_for("index"))


@app.route("/check_notification")
def check_notification():
    return render_template("check_notification.html")


@app.route("/notification_books")
def notification_books():
    path = HOME / "searching_books.json"
    email = request.args.get("email")
    searching_books = book.registered_books(email)
    if os.path.isfile(path) and searching_books:
        return render_template("notification_books.html", searching_books=searching_books)
    return render_template("not_registered.html")


@app.route("/cancel_notify/<title>/<email>")
def cancel_notify(title, email):
    mail.remove_email(title, email)
    return render_template("cancel_subscription.html", title=title)


if __name__ == '__main__':
    app.run(debug=True)
