import search_web


def test_check_for_book_status():
    status = search_web.check_for_book_status(
        url="https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=167B8I016255H.628999&profile=br-mar&uri=link=3100033~!2696598~!3100021~!3100029&aspect=basic_search&menu=search&ri=1&source=~!bracz&term=Gdzie+śpiewają+raki+%2F&index=ALTITLE")
    assert status == "24/03/2023"


def test_render_books():
    list_of_books = search_web.get_books(title="Zmierzch")
