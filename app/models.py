from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    assets = db.Column(db.JSON, default={'USD': 100.0, 'BTC': 0.0, 'ETH': 0.0, 'BNB': 0.0, 'XRP': 0.0, 'SOL': 0.0, 'ADA': 0.0, 'DOGE': 0.0, 'DOT': 0.0, 'EUR': 0.0, 'AMP': 0.0, 'PEPE': 0.0, 'LTC': 0.0})  # Инициализация по умолчанию

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_asset(self, asset_name: str, amount: float):
        if not hasattr(self, 'assets') or self.assets is None:
            self.assets = {}
        assets = dict(self.assets)
        assets[asset_name] = amount
        self.assets = assets

        db.session.add(self)
        db.session.commit()
    
class CurrencyPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    percent = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
