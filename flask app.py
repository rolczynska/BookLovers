from flask import Flask, render_template, request

from main import search_books
from address import get_url, check_for_book_status
from mail import send_mail, send_register_confirmation
from tools import add_to_list, is_already_registered, decode, HOME

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# TODO czy ta opcja z global jest poprawna?
@app.route("/answer")
def answer():
    title = request.args.get("title")
    url = get_url(title)
    availability = check_for_book_status(url)
    if availability:
        return render_template("book_available.html")
    return render_template("enter_email.html")


# TODO zrób template "already_registered.html"
@app.route("/enter_email", methods=["POST"])
def enter_email():
    url_title = request.referrer
    email = request.form.get("email")
    title = decode(url_title)
    if is_already_registered(title, email, path=HOME / "searching_books.json"):
        return render_template("already_registered.html")
    else:
        add_to_list(title, email, path=HOME / "searching_books.json")
        send_register_confirmation(title, email)
        return render_template("email_registered.html")
    # requests.post('http://127.0.0.1:5001/ ', data={'key': 'value'})

    # postawić drugą aplikacje która obsługuje szukanie po liście tytułów i wysyła maila.
    # Ma to być w oddzielnym folderze.


if __name__ == '__main__':
    app.run()
