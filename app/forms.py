from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import search_web


class BookForm(FlaskForm):
    title = StringField("Tytuł", validators=[DataRequired()])
    submit = SubmitField("Wyszukaj")

