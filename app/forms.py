from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20),
        Regexp(r'^[A-Za-z0-9а-яА-ЯёЁ]+$', message='Username must contain only letters (Latin or Cyrillic) or numbers')
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message='Please enter a valid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6),
        Regexp('^(?=.*[A-Za-z])(?=.*[!@#$%^&*(),.?":{}|<>])', message='Password must contain at least one letter and one special character')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Regexp(r'^[A-Za-zА-Яа-я0-9_-]+$', message="Username must contain only letters, numbers, and _ or - symbols.")
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')