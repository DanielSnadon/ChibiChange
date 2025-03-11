from flask import render_template, redirect, url_for, flash
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user


def register_routes(app):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            # Проверяем, есть ли пользователь с таким именем пользователя или email
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Username already taken, please choose another one', 'danger')
            else:
                existing_email = User.query.filter_by(email=form.email.data).first()
                if existing_email:
                    flash('Email already registered, please choose another one', 'danger')
                else:
                    # Создаем нового пользователя
                    new_user = User(username=form.username.data, email=form.email.data)
                    new_user.set_password(form.password.data)
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Registration successful! Please log in.', 'success')
                    return redirect(url_for('login'))
        else:
            # Если форма не прошла валидацию, выводим ошибки через flash
            for field, errors in form.errors.items():
                for error in errors:
                    flash(error, 'danger')
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            # Проверяем, существует ли пользователь с таким именем
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('home'))  # Перенаправление на домашнюю страницу
            else:
                flash('Invalid username or password', 'danger')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))  # Перенаправление на страницу входа
    
    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html', user=current_user)

    @app.route('/')
    def home():
        currencies = ["dollar", "euro", "linganguliguli"]
        return render_template('testiks.html', currencies=currencies)

