from flask import render_template, redirect, url_for, flash, request
from datetime import datetime, timedelta
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm, ChangePasswordForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import CurrencyPrice  # Новая модель для хранения цен


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

    @app.route("/")
    def home():
        # Получение текущих цен из парсера
        current_price_data = current_prices

        # Получение цен 24 часа назад из базы данных
        twenty_four_hours_ago = datetime.utcnow() - timedelta(minutes=15)
        old_prices = {}

        for currency_name in current_price_data.keys():
            price_record = (
                CurrencyPrice.query.filter(
                    CurrencyPrice.currency_name == currency_name,
                    CurrencyPrice.timestamp <= twenty_four_hours_ago,
                )
                .order_by(CurrencyPrice.timestamp.desc())
                .first()
            )

            if price_record:
                old_prices[currency_name] = price_record.price

        currencies = []
        for currency_name, current_price in current_price_data.items():
            # Сохранение текущей цены в базу
            price_record = CurrencyPrice(
                currency_name=currency_name,
                price=current_price,
                timestamp=datetime.utcnow(),
            )
            db.session.add(price_record)

            # Рассчитываем изменение за 24 часа
            change_percent = ""
            if currency_name in old_prices and old_prices[currency_name] != 0:
                change = (
                    (current_price - old_prices[currency_name])
                    / old_prices[currency_name]
                ) * 100
                change_percent = f"{change:+.2f}%"

            currencies.append(
                {
                    "name": currency_name,
                    "icon": get_currency_icon(
                        currency_name
                    ),  # Функция для получения иконки
                    "change": change_percent,
                    "price": f"{current_price:.2f}",
                    "current_price": current_price,
                    "old_price": old_prices.get(currency_name),
                }
            )

        db.session.commit()

        return render_template("testiks.html", currencies=currencies)

    @app.route("/currency/<currency_name>")
    def currency_detail(currency_name):

        return render_template("currency_detail.html", currency_name=currency_name)


def get_currency_icon(currency_name):
    icons = {
        "dollar": "💵",
        "euro": "💶",
        "yuan": "💴",
        "bitcoin": "₿",
        "linganguliguli": "🦁",
        "TUNG TUNG SAHUR": "🪵",
    }
    return icons.get(currency_name, "💰")
