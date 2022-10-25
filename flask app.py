from flask import Flask, render_template, request, session, redirect, url_for
from address import get_title_author_url, check_for_book_status
from mail import send_register_confirmation
from tools import add_to_list, is_already_registered,  HOME

app = Flask(__name__)
app.secret_key = "thisissession"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/confirm")
def confirm():
    title = request.args.get("title")
    web_title, web_author, url = get_title_author_url(title)
    session["title"] = web_title
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
    email = request.form.get("email")
    if is_already_registered(title, email, path=HOME / "searching_books.json"):
        return render_template("already_registered.html")
    else:
        add_to_list(title, email, path=HOME / "searching_books.json")
        # result 404 - not found
        # requests.get('http://localhost:4000/ ', data={title: email})
        send_register_confirmation(title, email)
        return render_template("email_registered.html")

    # postawić drugą aplikacje która obsługuje szukanie po liście tytułów i wysyła maila.
    # Ma to być w oddzielnym folderze.


if __name__ == '__main__':
    app.run(debug=True)
