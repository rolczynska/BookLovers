from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email
from dataclasses import dataclass


@dataclass
class Search:
    title: str
    author: str
    libraries: list
    email: str

    def libraries_and_mails_to_dict(self):
        dict_libraries = {library: [self.email] for library in self.libraries}
        return dict_libraries


class BookForm(FlaskForm):
    title = StringField("Tytuł", validators=[DataRequired()])
    submit = SubmitField("Wyszukaj")


class EmailForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),
                                             Email(message='Nieprawidłowy adres email')])
    submit = SubmitField("Zatwierdź")


class SignUpForm(FlaskForm):
    submit = SubmitField("Zapisz się do powiadomień!")
    checkbox = BooleanField(label="library")
