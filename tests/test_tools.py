import json
import os
import tools


def test_add_to_list():
    path = "fixtures/searching_books.json"
    tools.add_to_list("gdzie śpiewają raki", "olkiewicz.alex@gmail.com", path)
    with open(path) as file:
        result = json.load(file)
        assert result == {"gdzie śpiewają raki": ["olkiewicz.alex@gmail.com"]}

    tools.add_to_list("gdzie śpiewają raki", "olkiewicz.alex1234@gmail.com", path)
    with open(path) as file:
        result = json.load(file)
        assert result == {"gdzie śpiewają raki": ["olkiewicz.alex@gmail.com", "olkiewicz.alex1234@gmail.com"]}
    os.remove(path)


def test_is_already_registered():
    path = "fixtures/searching_books.json"
    tools.add_to_list("gdzie śpiewają raki", "olkiewicz.alex@gmail.com", path)
    result = tools.is_already_registered("gdzie śpiewają raki", "olkiewicz.alex@gmail.com", path)
    assert result

    result = tools.is_already_registered("gdzie śpiewają raki", "innymail@gami.com", path)
    assert not result

    result = tools.is_already_registered("365 dni", "olkiewicz.alex@gmail.com", path)
    assert not result
    os.remove(path)


def test_remove_email():
    path = "fixtures/searching_books.json"
    content = {"365 dni": ["olkiewicz.alex@gmail.com", "olkiewicz.alex1234@gmail.com"], "gdzie śpiewają raki": ["olkiewicz.alex@gmail.com"]}
    tools.json_dump(content, path)
    tools.remove_email("365 dni", "olkiewicz.alex1234@gmail.com", path)
    content = tools.json_load(path)
    assert content == {"365 dni": ["olkiewicz.alex@gmail.com"], "gdzie śpiewają raki": ["olkiewicz.alex@gmail.com"]}

    tools.remove_email("365 dni", "olkiewicz.alexees@gmail.com", path)
    content = tools.json_load(path)
    assert content == {"365 dni": ["olkiewicz.alex@gmail.com"], "gdzie śpiewają raki": ["olkiewicz.alex@gmail.com"]}

    tools.remove_email("567 dni", "olkiewicz.alexees@gmail.com", path)
    content = tools.json_load(path)
    assert content == {"365 dni": ["olkiewicz.alex@gmail.com"], "gdzie śpiewają raki": ["olkiewicz.alex@gmail.com"]}

    os.remove(path)


