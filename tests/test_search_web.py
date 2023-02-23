import search_web


def test_confirm_title_and_author():
    web_title, web_author, url = search_web.confirm_title_and_author(title="Zmierzch")
    assert web_title == "Zmierzch"


def test_display_books():
    list_of_books = search_web.render_books(title="Zmierzch")
