from app import create_app
from app.parser import update_prices
from threading import Thread
import time
from flask import Flask

app = create_app()

from app.routes import register_routes
register_routes(app)

def price_updater():
    """Фоновая задача для обновления цен"""
    while True:
        with app.app_context():
            update_prices()
        time.sleep(300)  # Интервал 5 минут

if __name__ == '__main__':
    updater_thread = Thread(target=price_updater, daemon=True)
    updater_thread.start()
    
    app.run(debug=True)