from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo,
    Email,
    Regexp,
    InputRequired,
)


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=20),
            Regexp(
                r"^[A-Za-z0-9а-яА-ЯёЁ]+$",
                message="Username must contain only letters (Latin or Cyrillic) or numbers",
            ),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Please enter a valid email address"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6),
            Regexp(
                '^(?=.*[A-Za-z])(?=.*[!@#$%^&*(),.?":{}|<>])',
                message="Password must contain at least one letter and one special character",
            ),
        ],
    )
    confirm_password = PasswordField(
        "ConFirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[InputRequired()])
    new_password = PasswordField(
        "New Password",
        validators=[
            InputRequired(),
            Length(min=6),
            Regexp(
                '^(?=.*[A-Za-z])(?=.*[!@#$%^&*(),.?":{}|<>])',
                message="Password must contain at least one letter and one special character",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            InputRequired(),
            EqualTo("new_password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Change Password")
