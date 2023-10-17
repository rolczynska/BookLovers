import threading
from flask import Flask, render_template, session, request

import booklovers.connect
from booklovers import connect, parser, forms, database, mail, notifications

# We create a Flask app.
app = Flask(__name__)
app.secret_key = "69430"  # a random number

# This is a loop for notification books.
notifications_loop = threading.Thread(target=notifications.main, daemon=True)
# notifications_loop.start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    # Search for books by a title.
    book_form = forms.BookForm(csrf_enabled=False)

    # If a form is validated, we search for books.
    if book_form.validate_on_submit():
        title = book_form.title.data

        page = connect.get_books_listing(title)
        books = parser.find_books(page)

        return render_template("display_books.html", books=books)
    return render_template("search.html", book_form=book_form)


@app.route("/availability/<string:title>?<string:author>", methods=["GET"])
def availability(title, author):
    # Checks and display current availability of a book in libraries in Poznań
    book_availability = booklovers.connect.get_libraries_availability(title, author)
    session["book_availability"] = book_availability
    return render_template("availability.html", book_availability=book_availability,
                           title=title, author=author)


@app.route("/sign_up/<string:title>?<string:author>", methods=["GET", "POST"])
def sign_up(title, author):
    # Sign up for notification for selected libraries
    sign_up_form = forms.SignUpForm(csrf_enabled=False)
    email_form = forms.EmailForm(csrf_enabled=False)
    book_availability = session["book_availability"]
    # If the form is validated we add the search to database
    if email_form.validate_on_submit():
        email = email_form.email.data
        chosen_libraries = request.form.getlist('checkbox')
        searches = forms.create_searches(title, author, chosen_libraries, email)
        database.add_to_database(searches)
        mail.send_register_confirmation(title, author, chosen_libraries, email)
        return render_template("email_registered.html")
    return render_template("sign_up.html", book_availability=book_availability,
                           email_form=email_form, sign_up_form=sign_up_form, book_title=title,
                           book_author=author)


@app.route("/check_notification", methods=["GET", "POST"])
def check_notification():
    # Checks user book notifications.
    email_form = forms.EmailForm(csrf_enabled=False)
    if email_form.validate_on_submit():
        email = email_form.email.data
        searches = database.get_searches(email)
        return render_template("notification_books.html", searches=searches)
    return render_template("check_notification.html", email_form=email_form)


@app.route("/cancel_notify/<title>/<author>/<email>")
def cancel_notify(title, author, email):
    # Cancels user book notifications.
    database.remove_search(title, author, email)
    return render_template("cancel_subscription.html", title=title)


if __name__ == '__main__':
    app.run(debug=True, port=5500)
