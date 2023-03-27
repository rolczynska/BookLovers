from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class BookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    submit = SubmitField("Search")


class EmailForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message='Invalid email address')])
    submit = SubmitField("Register for notification")
