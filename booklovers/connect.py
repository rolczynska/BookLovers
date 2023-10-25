import requests
from bs4 import BeautifulSoup


def get_page(url: str, username='spoxb565l6', password='3IpIum3wei9eOaoBl0') -> BeautifulSoup:
    """Gets the website using proxy. Return a parsed page by BeautifulSoup."""
    proxy = f'http://{username}:{password}@pl.smartproxy.com:20001'
    page = requests.get(url, proxies={'http': proxy, 'https': proxy})
    assert page.status_code == 200
    parsed_page = BeautifulSoup(page.text, "html.parser")
    return parsed_page


