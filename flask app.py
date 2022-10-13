from flask import Flask, render_template, request

import main
from address import get_url, check_for_book_status
from mail import send_mail, send_register_confirmation
from tools import add_to_list, is_already_registered, searching_titles

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# TODO czy ta opcja z global jest poprawna?
@app.route("/answer")
def answer():
    global title
    title = request.args.get("title")
    if not title:
        return render_template("failure.html")
    url = get_url(title)
    availability = check_for_book_status(url)
    if availability:
        return render_template("book_available.html")
    return render_template("enter_email.html")


# TODO zrób template "already_registered.html
@app.route("/enter_email", methods=["POST"])
def enter_email():
    email = request.form.get("email")
    if is_already_registered(title, email):
        return render_template("already_registered.html")
    else:
        add_to_list(title, email)
        send_register_confirmation(title, email)
        return render_template("email_registered.html")


if __name__ == '__main__':
    app.run()
    main.searching_books()

