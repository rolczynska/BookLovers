import search_web


def test_check_for_book_status():
    status = search_web.check_for_book_status(
        url="https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=167783M8340AG.457083&profile=br-mar&uri=link=3100033~!1939334~!3100021~!3100029&aspect=basic_search&menu=search&ri=1&source=~!bracz&term=Krzyżacy+%2F&index=ALTITLE")
    assert status == False


def test_render_books():
    list_of_books = search_web.render_books(title="Zmierzch")
