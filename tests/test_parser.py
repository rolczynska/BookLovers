from booklovers import parser, connect
from bs4 import BeautifulSoup


def test_find_books():
    with open("parsed_searching_page.html", "r") as file:
        parsed_page = BeautifulSoup(file, "html.parser")
        parser.find_books(parsed_page)


def test_check_for_book_status():
    list_urls = ["https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=1RQ703A004143.362212&profile=br-mar&uri=link=3100033~!2696598~!3100021~!3100029&aspect=basic_search&menu=search&ri=1&source=~!bracz&term=Gdzie+śpiewają+raki+%2F&index=ALTITLE", "https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=169C0310D59J3.362215&profile=br-mar&uri=link=3100033~!2849535~!3100021~!3100029&aspect=basic_search&menu=search&ri=1&source=~!bracz&term=Gdzie+śpiewają+raki+%2F&index=ALTITLE", "https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=1H9I03104I652.362217&profile=br-mar&uri=link=3100033~!2910511~!3100021~!3100029&aspect=basic_search&menu=search&ri=1&source=~!bracz&term=Gdzie+śpiewają+raki+%2F&index=ALTITLE"]
    parser.get_libraries_availability(list_urls)
