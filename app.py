import threading
from flask import Flask, render_template, session
from booklovers import connect, parser, forms, database, mail, notifications

# We create a Flask app.
app = Flask(__name__)
app.secret_key = "69430"  # a random number

# This is a loop for notification books.
notifications_loop = threading.Thread(target=notifications.run, daemon=True)
# notifications_loop.start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    # Search for books by title.
    book_form = forms.BookForm(csrf_enabled=False)

    # If a form is validated, we search for books.
    if book_form.validate_on_submit():
        title = book_form.title.data

        # We render links - list of books which contain this title
        # If the book is chosen we pass title and author to availability route
        page = connect.get_book_listing(title)
        books = parser.find_books(page)

        return render_template("display_books.html", books=books)
    return render_template("search.html", book_form=book_form)


@app.route("/availability/<string:book_title>?<string:book_author>", methods=["GET", "POST"])
def availability(book_title, book_author):
    # Checks and display the availability of a book in libraries in Poznań
    email_form = forms.EmailForm(csrf_enabled=False)
    book_urls = parser.get_urls(book_title, book_author)
    book_availability = parser.get_libraries_availability(book_urls)

    # If a form is validated, we add a book with email to database and render a page.
    if email_form.validate_on_submit():
        email = email_form.email.data
        database.add_to_registered(book_title, email)
        mail.send_register_confirmation(book_title, book_author, email)
        return render_template("email_registered.html")
    return render_template("availability.html", book_availability=book_availability,
                           book_title=book_title, book_author=book_author, email_form=email_form)


@app.route("/check_notification", methods=["GET", "POST"])
def check_notification():
    # Checks user book notifications.
    email_form = forms.EmailForm(csrf_enabled=False)
    if email_form.validate_on_submit():
        email = email_form.email.data
        books_dict = database.get_registered_books(email)
        return render_template("notification_books.html", books_dict=books_dict)
    return render_template("check_notification.html", email_form=email_form)


@app.route("/cancel_notify/<title>/<author>/<email>")
def cancel_notify(title, author, email):
    # Cancels user book notifications.
    database.remove_email(title, author, email)
    return render_template("cancel_subscription.html", title=title)


if __name__ == '__main__':
    app.run(debug=True, port=5500)
