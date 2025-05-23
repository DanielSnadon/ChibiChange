from flask import render_template, redirect, url_for, flash, request
from json import *
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
        return redirect(url_for("home"))

    @app.route('/profile')
    @login_required
    def profile():
        db.session.refresh(current_user)

        if not hasattr(current_user, 'assets') or current_user.assets is None:
            current_user.assets = {
                'USD': 0.0, 'BTC': 0.0, 'ETH': 0.0, 'BNB': 0.0,
                'XRP': 0.0, 'SOL': 0.0, 'ADA': 0.0, 'DOGE': 0.0,
                'DOT': 0.0, 'EUR': 0.0, 'AMP': 0.0, 'PEPE': 0.0,
                'LTC': 0.0
            }
            db.session.commit()
        
        currencies = create_curr()  # Получаем текущие цены
        
        usd_balance = current_user.assets.get('USD', 0.0)

        btc_amount = current_user.assets.get('BTC', 0.0)
        btc_price = currencies.get('BTC', {}).get('price', 0.0)
        btc_balance = btc_amount * btc_price

        eth_amount = current_user.assets.get('ETH', 0.0)
        eth_price = currencies.get('ETH', {}).get('price', 0.0)
        eth_balance = eth_amount * eth_price

        bnb_amount = current_user.assets.get('BNB', 0.0)
        bnb_price = currencies.get('BNB', {}).get('price', 0.0)
        bnb_balance = bnb_amount * bnb_price

        xrp_amount = current_user.assets.get('XRP', 0.0)
        xrp_price = currencies.get('XRP', {}).get('price', 0.0)
        xrp_balance = xrp_amount * xrp_price

        sol_amount = current_user.assets.get('SOL', 0.0)
        sol_price = currencies.get('SOL', {}).get('price', 0.0)
        sol_balance = sol_amount * sol_price

        ada_amount = current_user.assets.get('ADA', 0.0)
        ada_price = currencies.get('ADA', {}).get('price', 0.0)
        ada_balance = ada_amount * ada_price

        doge_amount = current_user.assets.get('DOGE', 0.0)
        doge_price = currencies.get('DOGE', {}).get('price', 0.0)
        doge_balance = doge_amount * doge_price

        dot_amount = current_user.assets.get('DOT', 0.0)
        dot_price = currencies.get('DOT', {}).get('price', 0.0)
        dot_balance = dot_amount * dot_price

        eur_amount = current_user.assets.get('EUR', 0.0)
        eur_price = currencies.get('EUR', {}).get('price', 0.0)
        eur_balance = eur_amount * eur_price

        amp_amount = current_user.assets.get('AMP', 0.0)
        amp_price = currencies.get('AMP', {}).get('price', 0.0)
        amp_balance = amp_amount * amp_price

        pepe_amount = current_user.assets.get('PEPE', 0.0)
        pepe_price = currencies.get('PEPE', {}).get('price', 0.0)
        pepe_balance = pepe_amount * pepe_price
        
        ltc_amount = current_user.assets.get('LTC', 0.0)
        ltc_price = currencies.get('LTC', {}).get('price', 0.0)
        ltc_balance = ltc_amount * ltc_price

        
        return render_template(
            "profile.html",
            user=current_user,
            usd_balance=usd_balance,
            btc_balance=round(btc_balance, 2),
            btc_amount=btc_amount,
            eth_balance=round(eth_balance, 2),
            eth_amount=eth_amount,
            bnb_balance=round(bnb_balance,2),
            bnb_amount=bnb_amount,
            xrp_balance=round(xrp_balance, 2),
            xrp_amount=xrp_amount,
            sol_balance=round(sol_balance, 2),
            sol_amount=sol_amount,
            ada_balance=round(ada_balance, 2),
            ada_amount=ada_amount,
            doge_balance=round(doge_balance, 2),
            doge_amount=doge_amount,
            dot_balance=round(dot_balance, 2),
            dot_amount=dot_amount,
            eur_balance=round(eur_balance, 2),
            eur_amount=eur_amount,
            amp_balance=round(amp_balance, 2),
            amp_amount=amp_amount,
            pepe_balance=round(pepe_balance, 2),
            pepe_amount=pepe_amount,
            ltc_balance=round(ltc_balance, 2),
            ltc_amount=ltc_amount,
        )

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
    
    @app.route('/buy_currency', methods=['POST'])
    @login_required
    def buy_currency():
        try:
            currency = request.form.get('currency', '').upper()
            amount_usd = float(request.form.get('amount', 0))
            
            db.session.refresh(current_user)
            
            usd_balance = current_user.assets.get('USD', 0.0)
            if usd_balance < amount_usd:
                flash(f'Insufficient USD balance. Your balance: {usd_balance:.2f} USD', 'error')
                return redirect(url_for('currency_detail', currency_name=currency.lower()))
            
            currencies = create_curr()
            exchange_rate = currencies.get(f"{currency}", {}).get('price', 0.0)
            
            if exchange_rate <= 0:
                flash('Invalid exchange rate', 'error')
                return redirect(url_for('currency_detail', currency_name=currency.lower()))
            
            currency_amount = amount_usd / exchange_rate
            
            current_user.update_asset('USD', usd_balance - amount_usd)
            current_user.update_asset(currency, round(current_user.assets.get(currency, 0.0) + currency_amount, 8))
            
            flash(f'Successfully bought {currency_amount:.8f} {currency}', 'success')
            return redirect(url_for('profile'))  # Перенаправляем на профиль
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('currency_detail', currency_name=currency.lower()))

    @app.route('/sell_currency', methods=['POST'])
    @login_required
    def sell_currency():
        try:
            currency = request.form.get('currency', '').upper()
            currency_amount = float(request.form.get('amount', 0))
            
            db.session.refresh(current_user)
            
            current_balance = current_user.assets.get(currency, 0.0)
            if current_balance < currency_amount:
                flash(f'Insufficient {currency} balance. Your balance: {current_balance:.8f} {currency}', 'error')
                return redirect(url_for('currency_detail', currency_name=currency.lower()))
            
            currencies = create_curr()
            exchange_rate = currencies.get(currency, {}).get('price', 0.0)
            
            if exchange_rate <= 0:
                flash('Invalid exchange rate', 'error')
                return redirect(url_for('currency_detail', currency_name=currency.lower()))
            
            amount_usd = currency_amount * exchange_rate
            
            current_user.update_asset(currency, current_balance - currency_amount)
            current_user.update_asset('USD', current_user.assets.get('USD', 0.0) + amount_usd)
            
            flash(f'Successfully sold {currency_amount:.8f} {currency} for {amount_usd:.2f} USD', 'success')
            return redirect(url_for('currency_detail', currency_name=currency.lower()))
            
        except ValueError:
            db.session.rollback()
            flash('Invalid amount format', 'error')
            return redirect(url_for('currency_detail', currency_name=currency.lower()))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('currency_detail', currency_name=currency.lower()))

    @app.route("/")
    def home():
        currencies = create_curr()
                
        return render_template("testiks.html", currencies=currencies)

    @app.route("/currency/<currency_name>")
    def currency_detail(currency_name):

        return render_template("currency_detail.html", currency_name=currency_name)
    
def create_curr():
    currencies = {}

    currency_names = db.session.query(CurrencyPrice.currency_name).distinct().all()
            
    for currency in currency_names:
        last_record = CurrencyPrice.query.filter_by(
            currency_name=currency[0]
        ).order_by(
            CurrencyPrice.timestamp.desc()
        ).first()
        
        if last_record:
            currencies[currency[0]] = {
                'percent': last_record.percent,
                'price': last_record.price
            }
    return currencies
