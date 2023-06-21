import threading
from flask import Flask, render_template, session
from booklovers import connect, parser, forms, database, mail, notifications

# We create a Flask app.
app = Flask(__name__)
app.secret_key = "69430"  # a random number

# This is a loop for searching demanded books.
demanded_books_loop = threading.Thread(target=notifications.run, daemon=True)
demanded_books_loop.start()


@app.route("/", methods=["GET", "POST"])
def index():
    # Search for books.
    book_form = forms.BookForm(csrf_enabled=False)

    # If a form is validated, we search for books and render them.
    if book_form.validate_on_submit():
        title = book_form.title.data

        # We get books from search module and save them in session.
        page = connect.get_book_listing(title)
        books = parser.find_books(page)
        session["books"] = books

        return render_template("display_books.html", books=books)
    return render_template("index.html", book_form=book_form)


@app.route("/availability/<int:book_index>", methods=["GET", "POST"])
def availability(book_index):
    # Checks the availability of a book.
    email_form = forms.EmailForm(csrf_enabled=False)
    book_params = session["books"][book_index]
    book = parser.Book(**book_params)
    date = parser.check_for_book_status(book.url)
    # If a form is validated, we add a book to demanded list and render a page.
    if email_form.validate_on_submit():
        email = email_form.email.data
        book_id = database.get_id(book)

        is_new = database.is_new_subscription(book_id, email)
        if is_new:
            database.add_to_registered(book_id, email)
            mail.send_register_confirmation(book.title, email)

        return render_template("email_registered.html")
    return render_template("availability.html", date=date, book=book, email_form=email_form)


@app.route("/check_notification", methods=["GET", "POST"])
def check_notification():
    # Checks user book notifications.
    email_form = forms.EmailForm(csrf_enabled=False)
    if email_form.validate_on_submit():
        email = email_form.email.data
        demanded_books = database.get_registered_books(email)

        return render_template("notification_books.html", demanded_books=demanded_books)
    return render_template("check_notification.html", email_form=email_form)


@app.route("/cancel_notify/<title>/<email>")
def cancel_notify(title, email):
    # Cancels user book notifications.
    mail.remove_email(title, email)
    return render_template("cancel_subscription.html", title=title)


if __name__ == '__main__':
    app.run(debug=True)
