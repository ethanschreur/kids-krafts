from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField 
from wtforms.validators import InputRequired, Email

class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    subject = StringField("Subject", validators=[InputRequired()])
    message = TextAreaField("Message", validators=[InputRequired()])