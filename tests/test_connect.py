from unittest.mock import patch, Mock
from booklovers.connect import get_page
from bs4 import BeautifulSoup


# Definiujemy funkcję zastępującą request.get (dodajemy możliwość przekazywania argumentów)
def mock_requests_get(*args, **kwargs):
    # tworzymy obiekt klasy Mock który ma różne atrybuty i go zwracamy
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><head><title>Test Page</title></head><body>Test Content</body></html>"
    return mock_response


# Dekorator patch sprawia, że gdy wywołujemy funkcję test_get_page i chcemy uzyskać odpowiedź
# request.get to wywołujemy mock_requests_get
@patch("booklovers.connect.requests.get", side_effect=mock_requests_get)
# przekazujemy do funkcji obiekt Mock, który zastępuje requests.get
def test_get_page(mock_get):
    url = "http://example.com"
    page = get_page(url)

    # Weryfikujemy czy funkcja mock_requests_get jeden raz wywołuje stronę z zawartym proxy
    proxy = f'http://spoxb565l6:3IpIum3wei9eOaoBl0@pl.smartproxy.com:20001'
    mock_get.assert_called_once_with(url, proxies={'http': proxy, 'https': proxy})

    # Sprawdzamy czy zwrócona page to obiekt klasy BeautifulSoup
    assert isinstance(page, BeautifulSoup)

    # Sprawdzamy czy w treści html jest zawarta oczekiwana treść
    assert page.title.string == "Test Page"
