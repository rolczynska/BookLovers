import pytest
from unittest.mock import patch, Mock

from booklovers.forms import Search, Book, Mail, EMAIL_ADDRESS, EMAIL_PASSWORD, EmailForm


class TestSearch:
    def test_change_to_dict(self):
        search = Search("Sample Book", "John Doe", ["Lib1", "Lib2"],
                        "test@example.com")

        result = search.change_to_dict()

        assert type(result) == dict
        assert result == {
            "title": "Sample Book",
            "author": "John Doe",
            "libraries": ["Lib1", "Lib2"],
            "email": "test@example.com"
        }

    def test_send_register_confirmation(self):
        @pytest.fixture
        def sample_search():
            return Search(title="Sample Title",
                          author="Sample Author",
                          libraries=["Library1", "Library2"],
                          email="sample@email.com")

        @patch("booklovers.forms.yagmail.SMTP")
        @patch("booklovers.forms.Environment")
        def test_send_register_confirmation(mock_environment, mock_smtp, sample_search):
            # Mocking the Jinja2 environment and template rendering
            mock_template = Mock()
            mock_template.render.return_value = "Rendered Content"
            mock_environment.return_value.get_template.return_value = mock_template

            # Calling the method
            sample_search.send_register_confirmation()

            # Asserting that yagmail.SMTP was initialized with expected parameters
            mock_smtp.assert_called_once_with(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)

            # Asserting that the send method of the SMTP object was called with expected parameters
            mock_smtp.return_value.send.assert_called_once_with(
                to="sample@email.com",
                subject='Zapisanie do subskrypcji BookLovers',
                contents="Rendered Content"
            )

            # Asserting the Jinja2 environment was setup and template was rendered with correct data
            mocked_env = mock_environment.return_value
            mocked_env.get_template.assert_called_once_with('mail_content.html')
            mock_template.render.assert_called_once_with(
                title="Sample Title",
                author="Sample Author",
                chosen_libraries=["Library1", "Library2"],
                email="sample@email.com"
            )

    def test_from_dict(self):
        data = {
            "title": "Sample Book",
            "author": "John Doe",
            "libraries": ["Lib1", "Lib2"],
            "email": "test@example.com"
        }
        search = Search.from_dict(data)

        assert search.title == "Sample Book"
        assert search.author == "John Doe"
        assert search.libraries == ["Lib1", "Lib2"]
        assert search.email == "test@example.com"

    def test_from_dict_missing_key(self):
        data = {
            "title": "Sample Title",
            "author": "Sample Author",
            "libraries": ["Lib1", "Lib2"]
            # email key is missing
        }
        with pytest.raises(KeyError):
            Search.from_dict(data)


class TestBook:
    def test_to_dict(self):
        book = Book(title="Sample Book", author="John Doe",
                    available_libraries=["Library1", "Library2"])

        book_dict = book.to_dict()

        expected_dict = {
            "Sample Book John Doe": ["Library1", "Library2"]
        }

        assert book_dict == expected_dict


class TestMail:
    def test_get_list_of_books(self):
        book_1 = Book("Sample Book", "John Doe", ["Library1", "Library2"])
        book_2 = Book("Sample Book_2", "John Black", ["Library5"])
        mail = Mail(email="test@example.com", books=[book_1, book_2])

        result = mail.get_list_of_books()
        expected_list = [book_1, book_2]
        assert result == expected_list

