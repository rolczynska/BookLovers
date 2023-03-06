import os
import re

from flask import Flask, render_template, request, session
from search_web import check_for_book_status, render_books
from mail import send_register_confirmation, remove_email
from tools import HOME
from main import search_books
from book import is_in_books_index, get_id, add_to_books_index, add_to_searching_list, is_mail_registered, registered_books
from unidecode import unidecode
import threading

# TODO zmień na jednolitą opcję importowania funkcji - czy poszczególne czy plik

app = Flask(__name__)
app.secret_key = "thisissession"

''' This is loop for searching books.'''
searching_books_loop = threading.Thread(target=search_books, daemon=True)
searching_books_loop.start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/display_books", methods=["GET", "POST"])
def display_books():
    if request.method == "POST":
        title = request.form["title"]
        books = render_books(title)
        session["books"] = books
        return render_template("display_books.html", books=books)
    else:
        return render_template("index.html")


@app.route("/availability/<book_index>")
def availability(book_index):
    book_index = int(book_index)
    books = session["books"]
    url = books[book_index][0]
    session["url"] = url
    title = unidecode(books[book_index][1]).strip(" /")
    session["title"] = title
    author = unidecode(books[book_index][2])
    stripped_author = re.sub(r'\([^)]*\)', '', author).strip(" .")
    session["author"] = stripped_author
    date = check_for_book_status(url)
    if date == "Na półce":
        return render_template("book_available.html", title=title, author=stripped_author)
    elif date == "":
        return render_template("no_book.html")
    else:
        return render_template("enter_email.html", date=date)


@app.route("/enter_email", methods=["POST"])
def enter_email():
    title = session["title"]
    url = session["url"]
    author = session["author"]
    session["email"] = request.form.get("email")
    email = session["email"]
    if is_in_books_index(title, author, path=HOME / "books_index.json"):
        book_id = get_id(title, author, path=HOME / "books_index.json")
        if is_mail_registered(book_id, email):
            return render_template("already_registered.html")
    else:
        book_id = add_to_books_index(title, author, url, path=HOME / "books_index.json")
    add_to_searching_list(book_id, email, path=HOME / "searching_books.json")
    send_register_confirmation(title, email)
    return render_template("email_registered.html")


@app.route("/check_notification")
def check_notification():
    return render_template("check_notification.html")


@app.route("/notification_books")
def notification_books():
    path = HOME / "searching_books.json"
    email = request.args.get("email")
    searching_books = registered_books(email)
    if os.path.isfile(path) and searching_books:
        return render_template("notification_books.html", searching_books=searching_books)
    return render_template("not_registered.html")


@app.route("/cancel_notify/<title>/<email>")
def cancel_notify(title, email):
    remove_email(title, email)
    return render_template("cancel_subscription.html", title=title)


if __name__ == '__main__':
    app.run(debug=True)
