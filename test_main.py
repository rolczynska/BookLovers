import main


def test_search_for_status():
    result = main.search_for_status(urls={"365 dni": 'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=1I6N352V98223.87243&profile=br-mar&uri=link=3100033~!2651526~!3100021~!3100029'})
    assert result == {"365 dni": ["Wypożyczony", "Na półce"]}


def test_check_is_it_available():
    result = main.check_is_it_available({"Osiem randek": ["Wypożyczony"], "365 dni": ["Wypożyczony", "Na półce"]})
    assert result == ["365 dni"]


def test_send_mail():
    main.send_mail(["Super", "Ola", "Rafał"])
