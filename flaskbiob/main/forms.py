from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired()])
    email = StringField("Your email address", validators=[DataRequired(), Email()])
    message = TextAreaField("Your message", validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField("Send message")
