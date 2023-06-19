import json
import os

import book
import mail
import tools


def test_add_to_list():
    path = "fixtures/searching_books.json"
    book.add_to_registered("gdzie śpiewają raki", "olkiewicz.alex@gmail.com", path)
    with open(path) as file:
        result = json.load(file)
        assert result == {"gdzie śpiewają raki": ["olkiewicz.alex@gmail.com"]}

    book.add_to_registered("gdzie śpiewają raki", "olkiewicz.alex1234@gmail.com", path)
    with open(path) as file:
        result = json.load(file)
        assert result == {"gdzie śpiewają raki": ["olkiewicz.alex@gmail.com", "olkiewicz.alex1234@gmail.com"]}
    os.remove(path)


def test_is_already_registered():
    path = "fixtures/searching_books.json"
    book.add_to_registered("gdzie śpiewają raki", "olkiewicz.alex@gmail.com", path)
    result = book.is_mail_registered("gdzie śpiewają raki", "olkiewicz.alex@gmail.com", path)
    assert result

    result = book.is_mail_registered("gdzie śpiewają raki", "innymail@gami.com", path)
    assert not result

    result = book.is_mail_registered("365 dni", "olkiewicz.alex@gmail.com", path)
    assert not result
    os.remove(path)


def test_remove_email():
    path = "fixtures/searching_books.json"
    content = {"365 dni": ["olkiewicz.alex@gmail.com", "olkiewicz.alex1234@gmail.com"], "gdzie śpiewają raki": ["olkiewicz.alex@gmail.com"]}
    tools.json_dump(content, path)
    mail.remove_email("365 dni", "olkiewicz.alex1234@gmail.com", path)
    content = tools.json_load(path)
    assert content == {"365 dni": ["olkiewicz.alex@gmail.com"], "gdzie śpiewają raki": ["olkiewicz.alex@gmail.com"]}

    mail.remove_email("365 dni", "olkiewicz.alexees@gmail.com", path)
    content = tools.json_load(path)
    assert content == {"365 dni": ["olkiewicz.alex@gmail.com"], "gdzie śpiewają raki": ["olkiewicz.alex@gmail.com"]}

    mail.remove_email("567 dni", "olkiewicz.alexees@gmail.com", path)
    content = tools.json_load(path)
    assert content == {"365 dni": ["olkiewicz.alex@gmail.com"], "gdzie śpiewają raki": ["olkiewicz.alex@gmail.com"]}

    os.remove(path)


def test_add_a_book():
    tools.add_to_book_ids(book_url='https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=16773N302089J.374763&profile=br-mar&uri=link=3100033~!2475995~!3100021~!3100029&aspect=basic_search&menu=search&ri=1&source=~!bracz&term=Światło%2C+którego+nie+widać+%2F&index=ALTITLE',
                          title="Swiatlo, ktorego nie widac", author="Anthony Doer", path=tools.HOME / "books_id.json")
    content = tools.json_load(path=tools.HOME / "books_id.json")
    assert content == {
   "1": [
      "https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=16773N302089J.374763&profile=br-mar&uri=link=3100033~!2475995~!3100021~!3100029&aspect=basic_search&menu=search&ri=1&source=~!bracz&term=\u015awiat\u0142o%2C+kt\u00f3rego+nie+wida\u0107+%2F&index=ALTITLE",
      "Swiatlo, ktorego nie widac",
      "Anthony Doer"
   ]}

    tools.add_to_book_ids(book_url='https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=16E733O4872L3.375104&profile=br-mar&uri=link=3100033~!2102464~!3100021~!3100029&aspect=basic_search&menu=search&ri=1&source=~!bracz&term=Zmierzch+%2F&index=ALTITLE',
                          title="Zmierzch", author="Meyer, Stephanie", path=tools.HOME / "books_id.json")
    content = tools.json_load(path=tools.HOME / "books_id.json")
    assert content == {
   "1": [
      "https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=16773N302089J.374763&profile=br-mar&uri=link=3100033~!2475995~!3100021~!3100029&aspect=basic_search&menu=search&ri=1&source=~!bracz&term=\u015awiat\u0142o%2C+kt\u00f3rego+nie+wida\u0107+%2F&index=ALTITLE",
      "Swiatlo, ktorego nie widac",
      "Anthony Doer"
   ],
   "2": [
      "https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=16E733O4872L3.375104&profile=br-mar&uri=link=3100033~!2102464~!3100021~!3100029&aspect=basic_search&menu=search&ri=1&source=~!bracz&term=Zmierzch+%2F&index=ALTITLE",
      "Zmierzch",
      "Meyer, Stephanie"
   ]
    }
    os.remove(path=tools.HOME / "books_id.json")



