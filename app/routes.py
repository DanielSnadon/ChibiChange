from flask import render_template, redirect, url_for, flash, request
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm, ChangePasswordForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


def register_routes(app):
    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            # Проверяем, есть ли пользователь с таким именем пользователя или email
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash("Username already taken, please choose another one", "danger")
            else:
                existing_email = User.query.filter_by(email=form.email.data).first()
                if existing_email:
                    flash(
                        "Email already registered, please choose another one", "danger"
                    )
                else:
                    # Создаем нового пользователя
                    new_user = User(username=form.username.data, email=form.email.data)
                    new_user.set_password(form.password.data)
                    db.session.add(new_user)
                    db.session.commit()
                    flash("Registration successful! Please log in.", "success")
                    return redirect(url_for("login"))
        else:
            # Если форма не прошла валидацию, выводим ошибки через flash
            for field, errors in form.errors.items():
                for error in errors:
                    flash(error, "danger")
        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            # Проверяем, существует ли пользователь с таким именем
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for("home"))  # Перенаправление на домашнюю страницу
            else:
                flash("Invalid username or password", "danger")
        return render_template("login.html", form=form)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("home"))  # Перенаправление на страницу входа

    @app.route("/profile")
    @login_required
    def profile():
        return render_template("profile.html", user=current_user)

    @app.route("/settings")
    @login_required
    def settings():
        return render_template("settings.html", user=current_user)

    @app.route("/change_password", methods=["GET", "POST"])
    @login_required
    def change_password():
        form = ChangePasswordForm()

        if form.validate_on_submit():
            current_password = form.current_password.data
            new_password = form.new_password.data
            confirm_password = form.confirm_password.data

            # Проверка, что новый пароль и подтверждение совпадают
            if new_password != confirm_password:
                flash("New password and confirmation do not match!", "danger")
                return redirect(url_for("change_password"))

            # Проверка текущего пароля
            if not check_password_hash(current_user.password_hash, current_password):
                flash("Current password is incorrect!", "danger")
                return redirect(url_for("change_password"))

            # Хеширование нового пароля и обновление в базе данных
            hashed_password = generate_password_hash(new_password)
            current_user.password_hash = hashed_password
            db.session.commit()

            flash("Your password has been successfully changed!", "success")
            return redirect(url_for("change_password"))

        # Если форма не прошла валидацию, выводим ошибки через flash
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, "danger")

        return render_template("change_password.html", form=form)

    @app.route('/')
    def home():
        currencies = [
            {"name": "dollar", "icon": "💵", "description": "US Dollar"},
            {"name": "euro", "icon": "💶", "description": "European Euro"},
            {"name": "linganguliguli", "icon": "🦁", "description": "TRALALELO TRALALA"},
            {"name": "TUNG TUNG SAHUR", "icon": "🪵", "description": "tung tung tung tung tung tung tung tung tung sahur"},
        ]
        return render_template('testiks.html', currencies=currencies)

    @app.route("/currency/<currency_name>")
    def currency_detail(currency_name):

        return render_template("currency_detail.html", currency_name=currency_name)
