from app import create_app
from app.Pars import parser_start
from app.GrapgBigBuilder import big_graph
from app.GraphBuilder import graph
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
            parser_start()
            time.sleep(10)  # Интервал 5 минут
            graph()
            big_graph()


if __name__ == "__main__":
    updater_thread = Thread(target=price_updater, daemon=True)
    updater_thread.start()

    app.run(debug=True)
