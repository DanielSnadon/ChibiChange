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

    @app.route("/profile")
    @login_required
    def profile():
        db.session.refresh(current_user)

        if not hasattr(current_user, "assets") or current_user.assets is None:
            current_user.assets = {
                "USD": 0.0,
                "BTC": 0.0,
                "ETH": 0.0,
                "BNB": 0.0,
                "XRP": 0.0,
                "SOL": 0.0,
                "ADA": 0.0,
                "DOGE": 0.0,
                "DOT": 0.0,
                "EUR": 0.0,
                "AMP": 0.0,
                "PEPE": 0.0,
                "LTC": 0.0,
            }
            db.session.commit()

        currencies = create_curr()  # Получаем текущие цены

        usd_balance = current_user.assets.get("USD", 0.0)

        btc_amount = current_user.assets.get("BTC", 0.0)
        btc_price = currencies.get("BTC", {}).get("price", 0.0)
        btc_balance = btc_amount * btc_price

        eth_amount = current_user.assets.get("ETH", 0.0)
        eth_price = currencies.get("ETH", {}).get("price", 0.0)
        eth_balance = eth_amount * eth_price

        bnb_amount = current_user.assets.get("BNB", 0.0)
        bnb_price = currencies.get("BNB", {}).get("price", 0.0)
        bnb_balance = bnb_amount * bnb_price

        xrp_amount = current_user.assets.get("XRP", 0.0)
        xrp_price = currencies.get("XRP", {}).get("price", 0.0)
        xrp_balance = xrp_amount * xrp_price

        sol_amount = current_user.assets.get("SOL", 0.0)
        sol_price = currencies.get("SOL", {}).get("price", 0.0)
        sol_balance = sol_amount * sol_price

        ada_amount = current_user.assets.get("ADA", 0.0)
        ada_price = currencies.get("ADA", {}).get("price", 0.0)
        ada_balance = ada_amount * ada_price

        doge_amount = current_user.assets.get("DOGE", 0.0)
        doge_price = currencies.get("DOGE", {}).get("price", 0.0)
        doge_balance = doge_amount * doge_price

        dot_amount = current_user.assets.get("DOT", 0.0)
        dot_price = currencies.get("DOT", {}).get("price", 0.0)
        dot_balance = dot_amount * dot_price

        eur_amount = current_user.assets.get("EUR", 0.0)
        eur_price = currencies.get("EUR", {}).get("price", 0.0)
        eur_balance = eur_amount * eur_price

        amp_amount = current_user.assets.get("AMP", 0.0)
        amp_price = currencies.get("AMP", {}).get("price", 0.0)
        amp_balance = amp_amount * amp_price

        pepe_amount = current_user.assets.get("PEPE", 0.0)
        pepe_price = currencies.get("PEPE", {}).get("price", 0.0)
        pepe_balance = pepe_amount * pepe_price

        ltc_amount = current_user.assets.get("LTC", 0.0)
        ltc_price = currencies.get("LTC", {}).get("price", 0.0)
        ltc_balance = ltc_amount * ltc_price

        return render_template(
            "profile.html",
            user=current_user,
            usd_balance=usd_balance,
            btc_balance=round(btc_balance, 2),
            btc_amount=btc_amount,
            eth_balance=round(eth_balance, 2),
            eth_amount=eth_amount,
            bnb_balance=round(bnb_balance, 2),
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

    @app.route("/buy_currency", methods=["POST"])
    @login_required
    def buy_currency():
        try:
            currency = request.form.get("currency", "").upper()
            amount_usd = float(request.form.get("amount", 0))

            db.session.refresh(current_user)

            usd_balance = current_user.assets.get("USD", 0.0)
            if usd_balance < amount_usd:
                flash(
                    f"Insufficient USD balance. Your balance: {usd_balance:.2f} USD",
                    "error",
                )
                return redirect(
                    url_for("currency_detail", currency_name=currency.lower())
                )

            currencies = create_curr()
            exchange_rate = currencies.get(f"{currency}", {}).get("price", 0.0)

            if exchange_rate <= 0:
                flash("Invalid exchange rate", "error")
                return redirect(
                    url_for("currency_detail", currency_name=currency.lower())
                )

            currency_amount = amount_usd / exchange_rate

            current_user.update_asset("USD", usd_balance - amount_usd)
            current_user.update_asset(
                currency,
                round(current_user.assets.get(currency, 0.0) + currency_amount, 8),
            )

            flash(f"Successfully bought {currency_amount:.8f} {currency}", "success")
            return redirect(url_for("profile"))  # Перенаправляем на профиль

        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for("currency_detail", currency_name=currency.lower()))

    @app.route("/sell_currency", methods=["POST"])
    @login_required
    def sell_currency():
        try:
            currency = request.form.get("currency", "").upper()
            currency_amount = float(request.form.get("amount", 0))

            db.session.refresh(current_user)

            current_balance = current_user.assets.get(currency, 0.0)
            if current_balance < currency_amount:
                flash(
                    f"Insufficient {currency} balance. Your balance: {current_balance:.8f} {currency}",
                    "error",
                )
                return redirect(
                    url_for("currency_detail", currency_name=currency.lower())
                )

            currencies = create_curr()
            exchange_rate = currencies.get(currency, {}).get("price", 0.0)

            if exchange_rate <= 0:
                flash("Invalid exchange rate", "error")
                return redirect(
                    url_for("currency_detail", currency_name=currency.lower())
                )

            amount_usd = currency_amount * exchange_rate

            current_user.update_asset(currency, current_balance - currency_amount)
            current_user.update_asset(
                "USD", current_user.assets.get("USD", 0.0) + amount_usd
            )

            flash(
                f"Successfully sold {currency_amount:.8f} {currency} for {amount_usd:.2f} USD",
                "success",
            )
            return redirect(url_for("currency_detail", currency_name=currency.lower()))

        except ValueError:
            db.session.rollback()
            flash("Invalid amount format", "error")
            return redirect(url_for("currency_detail", currency_name=currency.lower()))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for("currency_detail", currency_name=currency.lower()))

    @app.route("/")
    def home():
        currencies = create_curr()

        return render_template("testiks.html", currencies=currencies)

    @app.route("/currency/<currency_name>")
    def currency_detail(currency_name):
        descriptions = {
            "BTC": "Bitcoin (BTC) is one of the most popular cryptocurrencies in the market. First introduced in 2009 by Satoshi Nakamoto, Bitcoin continues to be the top cryptocurrency by market capitalization. Bitcoin paved the way for many existing altcoins in the market and marked a pivotal moment for digital payment solutions.",
            "ETH": "Ethereum (ETH) is the second-largest cryptocurrency by market capitalization, known for introducing smart contracts, decentralized finance (DeFi), and decentralized applications (DApps). Since its launch in 2015 by Vitalik Buterin, Ethereum has set to revolutionize the blockchain industry by enabling decentralized applications to run on a global network of nodes.",
            "BNB": "BNB is a cryptocurrency that can be used to trade and pay fees on the Binance cryptocurrency exchange. BNB is also the cryptocurrency coin that powers the BNB Chain ecosystem. As one of the world's most popular utility tokens, BNB is useful to users in a wide range of applications and use cases.",
            "XRP": "XRP is the native digital asset on the XRP Ledger (XRPL) blockchain, built originally for payments. XRP primarily facilitates transactions on the network and bridges currencies in the XRP Ledger's native DEX. XRP is a digital asset that’s native to the XRP Ledger—an open-source, permissionless and decentralized blockchain technology.",
            "SOL": "Solana is a Layer-1 blockchain aimed to deliver high speed and efficiency while supporting smart contracts. It is a platform designed for hosting decentralized and scalable applications, making it a popular choice for developers and users alike.",
            "ADA": "Cardano is a third-generation proof-of-stake blockchain platform and home to ADA cryptocurrency: the first to be founded on peer-reviewed research and developed through evidence-based methods. It combines pioneering technologies, including a unique two-layer architecture, to provide unparalleled security.",
            "DOGE": "Dogecoin (DOGE) was introduced in 2013 as a fun alternative to traditional cryptocurrencies like Bitcoin. Its name and logo are inspired by a popular meme, reflecting its playful origins. Unlike Bitcoin, which emphasizes scarcity, Dogecoin is designed to be abundant in supply, with 10,000 new coins mined every minute and no cap on its total supply.",
            "DOT": "Polkadot (DOT) is a blockchain launched in 2016 by Gavin Wood, Ethereum's former CTO and co-founder. It allows developers to create customized interoperable parachains, or blockchains deployed from the Polkadot mainnet. Each parachain connects to the main relay chain, allowing them to communicate and share in the security measures of the mainnet.",
            "EUR": "Euro (EUR) is the official currency of 20 of the 27 member states of the European Union. The name euro was officially adopted on 16 December 1995 in Madrid. The euro was introduced to world financial markets as an accounting currency on 1 January 1999, replacing the former European Currency Unit (ECU) at a ratio of 1:1.",
            "AMP": "AMP is an ERC-20 token used to collateralize payments on the Flexa asset transfer network. As Flexa’s exclusive collateral token, AMP is used to minimize risk between counter-parties in transactions and facilitate crypto-collateralized payments at virtually any retail or online location. AMP price is updated on Binance in real time.",
            "PEPE": "The PEPE coin is a meme coin built upon the legacy of Pepe the Frog, a popular internet character. The cryptocurrency draws on the lighthearted and humorous nature of the meme to create a unique and engaging digital asset. Built on the Ethereum blockchain, the project seeks to leverage the success of meme coins, such as Shiba Inu and Dogecoin, and aims to become a leading meme-based cryptocurrency.",
            "LTC": "Litecoin (LTC) is a peer-to-peer (P2P) payments cryptocurrency that was forked from Bitcoin in 2011. As one of the earliest cryptocurrencies after Bitcoin, it is one of the first altcoins and allows users to send payments quickly and easily. While Litecoin shares many similarities with Bitcoin, it is designed to deliver a more efficient means of sending and receiving P2P payments and is accepted by thousands of retailers and merchants globally.",
        }
        currencies = create_curr()
        return render_template(
            "currency_detail.html",
            currency_name=currency_name,
            descriptions=descriptions,
            currencies=currencies,
        )


def create_curr():
    currencies = {}

    currency_names = db.session.query(CurrencyPrice.currency_name).distinct().all()

    for currency in currency_names:
        last_record = (
            CurrencyPrice.query.filter_by(currency_name=currency[0])
            .order_by(CurrencyPrice.timestamp.desc())
            .first()
        )

        if last_record:
            currencies[currency[0]] = {
                "percent": last_record.percent,
                "price": last_record.price,
            }
    return currencies
