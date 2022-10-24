import address
import pytest


def test_get_url():
    result = address.get_title_author_url("365 dni")
    assert result == "https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=166B5852R74W9.199857&amp;profile=br-mar&amp;uri=link=3100033~!2651526~!3100021~!3100029&amp;aspect=basic_search&amp;menu=search&amp;ri=1&amp;source=~!bracz&amp;term=365+dni+%2F&amp;index=ALTITLE"