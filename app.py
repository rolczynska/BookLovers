import threading
from flask import Flask, render_template, session, request
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


@app.route("/availability/<string:title>?<string:author>", methods=["GET"])
def availability(title, author):
    # Checks and display the availability of a book in libraries in Poznań
    book_urls = parser.get_urls(title, author)
    book_availability = parser.get_libraries_availability(book_urls)
    # create_a_sign_up_submit_button
    session["book_availability"] = book_availability
    return render_template("availability.html", book_availability=book_availability,
                           title=title, author=author)


@app.route("/sign_up/<string:title>?<string:author>", methods=["GET", "POST"])
def sign_up(title, author):
    sign_up_form = forms.SignUpForm(csrf_enabled=False)
    email_form = forms.EmailForm(csrf_enabled=False)
    book_availability = session["book_availability"]
    libraries_for_sign_up = parser.get_libraries_for_sign_up(book_availability)
    if email_form.validate_on_submit():
        email = email_form.email.data
        chosen_libraries = request.form.getlist('checkbox')

        search = forms.Search(title, author, chosen_libraries, email)
        database_data = change_to_database_object(search)
        database.add_to_registered(search)
        mail.send_register_confirmation(title, author, chosen_libraries, email)
        return render_template("email_registered.html")
    return render_template("sign_up.html", libraries_for_sign_up=libraries_for_sign_up,
                           email_form=email_form, sign_up_form=sign_up_form, book_title=title,
                           book_author=author)


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
