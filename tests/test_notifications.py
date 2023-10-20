from booklovers import notifications, forms


def test_get_available_libraries():
    search = forms.Search(title='W pustyni i w puszczy', author='Sienkiewicz, Henryk',
                          libraries=['F02 os.Oswiecenia 59 tel. 61 8767121',
                                     'F06 Tomickiego 14 tel. 61 8771455',
                                     'F15 Fabianowo 2 tel. 61 8304016',
                                     'F62 os.Sobieskiego paw.103 tel. 61 8252075',
                                     'F11dz Al. Marcinkowskiego 23'],
                          email='olkiewicz.alex1234@gmail.com')
    availability = {'F04 Lodowa 4 tel. 61 8662452': ['Na półce', '\xa0'],
                    'MHS Stary Rynek 84 tel. 61 8528971': ['Czytelnia', '\xa0'],
                    'F49 os.Pod Lipami tel. 61 8770637': ['Wypożyczony', '31/12/2020'],
                    'F62 os.Sobieskiego paw.103 tel. 61 8252075': ['Wypożyczony', '13/11/2023'],
                    'Czytelnia Al. Marcinkowskiego 23': ['Na półce', ''],
                    'F02 os.Oswiecenia 59 tel. 61 8767121': ['Wypożyczony', '13/11/2023'],
                    'F11dz Al. Marcinkowskiego 23': ['Na półce', ''],
                    'FW/53 ul. Hetmanska 91 tel. 61 8337140': ['Na półce', '\xa0'],
                    'F06 Tomickiego 14 tel. 61 8771455': ['Wypożyczony', '06/11/2023'],
                    'F55 os.Zwyciestwa 125 tel. 61 8230551': ['Na półce', ''],
                    'F42 os.Pod Lipami tel. 61 8200793': ['Na półce', ''],
                    'F15 Fabianowo 2 tel. 61 8304016': ['Na półce', '\xa0'],
                    'F12/46 Arciszewskiego 27 tel. 61 8627715': ['Na półce', '\xa0'],
                    'F51 os.Lecha 15 tel. 61 8777521': ['Na półce', '\xa0'],
                    'F50 os.Kosmonautow "Orbita" tel. 61 8205921': ['Na półce', '']}

    result = notifications.get_available_libraries(search=search, availability=availability)
    assert 'F11dz Al. Marcinkowskiego 23' in result
    assert 'F15 Fabianowo 2 tel. 61 8304016' in result
