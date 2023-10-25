from booklovers.database import create_unique_id
from booklovers import forms


def test_create_unique_id():
    result = create_unique_id("abcde", "fghij", "klmno")
    assert result == 'ab5defg5ijkl5no'