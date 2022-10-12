from flask import Flask, render_template, request
from address import get_url, search_for_book_status, send_mail
app = Flask(__name__)


searching_books = []

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/answer")
def answer():
    title = request.args.get("title")
    if not title:
        return render_template("failure.html")
    url = get_url(title)
    availability = search_for_book_status(url)
    if availability:
        return render_template("book_available.html")
    searching_books.append(title)
    return render_template("enter_email.html")


@app.route("/answer/enter_email", methods=["POST"])
def enter_email():
    email = request.form.get("email")
    send_mail(email, searching_books[-1])
    return render_template("email_registered.html")


if __name__ == '__main__':
    app.run()
