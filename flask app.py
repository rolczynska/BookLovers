from flask import Flask, render_template, request, session
from search_web import check_for_book_status, render_books
from mail import send_register_confirmation
from tools import add_to_list, is_already_registered,  HOME, json_load, remove_email
from main import search_books
import threading

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
    """Teraz tytuł i url zostanie przekzany na podstawie wyboru użytkownika - w co kliknie na wyświetlanej stronie."""
    if request.method == "POST":
        title = request.form["title"]
        books = render_books(title)
        session["books"] = books
        return render_template("display_books.html", books=books)
    else:
        return render_template("index.html")


@app.route("/availability/<book_id>")
def availability(book_id):
    book_id = int(book_id)
    books = session["books"]
    book_url = books[book_id][0]
    title = books[book_id][1]
    author = books[book_id][2]
    availability = check_for_book_status(book_url)
    if availability:
        return render_template("book_available.html", title=title, author=author)
    return render_template("enter_email.html")


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


@app.route("/check_notification")
def check_notification():
    return render_template("check_notification.html")


@app.route("/notification_books")
def notification_books():
    path = HOME / "searching_books.json"
    email = request.args.get("email")
    searching_books = []
    if os.path.isfile(path):
        content = json_load(path)
        for title, emails in content.items():
            if email in emails:
                searching_books.append(title)
        if searching_books:
            return render_template("notification_books.html", searching_books=searching_books)
    return render_template("not_registered.html")


@app.route("/cancel_notify/<title>/<email>")
def cancel_notify(title, email):
    remove_email(title, email)
    return render_template("cancel_subscription.html", title=title)


if __name__ == '__main__':
    app.run(debug=True)
