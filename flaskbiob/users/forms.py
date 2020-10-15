from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskbiob.models import Users


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("User already exists")

    def validate_email(self, email):
        email = Users.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("User account with this email already exists")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log in")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Save Changes")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("User already exists")

    def validate_email(self, email):
        if email.data != current_user.email:
            email = Users.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("User account with this email already exists")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request password reset email")

    def validate_email(self, email):
        email = Users.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError("No account with this address")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Confirm password reset")