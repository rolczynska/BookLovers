from flask import Flask, render_template, request, session, redirect, url_for
from search_web import confirm_title_and_author, check_for_book_status
from mail import send_register_confirmation
from tools import add_to_list, is_already_registered,  HOME, json_load, remove_email
import os
from unidecode import unidecode

app = Flask(__name__)
app.secret_key = "thisissession"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/confirm")
def confirm():
    title = request.args.get("title")
    web_title, web_author, url = confirm_title_and_author(title)
    session["title"] = unidecode(web_title).strip(" /")
    session["url"] = url
    return render_template("confirm.html", web_title=web_title, web_author=web_author)


@app.route("/answer")
def answer():
    if "title" in session:
        title = session["title"]
        url = session["url"]
        availability = check_for_book_status(url)
        if availability:
            return render_template("book_available.html", title=title)
        return render_template("enter_email.html")
    else:
        return redirect(url_for("/"))


@app.route("/no_book")
def no_book():
    return render_template("no_book.html")


@app.route("/enter_email", methods=["POST"])
def enter_email():
    title = session["title"]
    session["email"] = request.form.get("email")
    email = session["email"]
    if is_already_registered(title, email, path=HOME / "searching_books.json"):
        return render_template("already_registered.html")
    else:
        add_to_list(title, email, path=HOME / "searching_books.json")
        send_register_confirmation(title, email)
        return render_template("email_registered.html")

    # postawić drugą aplikacje która obsługuje szukanie po liście tytułów i wysyła maila.
    # Ma to być w oddzielnym folderze.


@app.route("/my_notification")
def my_notification():
    return render_template("my_notification.html")


@app.route("/searching_books")
def searching_books():
    path = HOME / "searching_books.json"
    email = request.args.get("email")
    searching_books = []
    if os.path.isfile(path):
        content = json_load(path)
        for title, emails in content.items():
            if email in emails:
                searching_books.append(title)
        if searching_books:
            return render_template("searching_books.html", searching_books=searching_books)
    return render_template("not_registered.html")


@app.route("/cancel_notify/<title>/<email>")
def cancel_notify(title, email):
    remove_email(title, email)
    return render_template("cancel_subscription.html", title=title)


if __name__ == '__main__':
    app.run(debug=True)
