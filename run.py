from app import create_app
from app.Pars import parser_start
from app.GrapgBigBuilder import big_graph
from app.GraphBuilder import graph
from threading import Thread
import time
from flask import Flask
from app import db

app = create_app()

from app.routes import register_routes

register_routes(app)


def price_updater():
    while True:
        with app.app_context():
            try:
                parser_start()
                graph()
                big_graph()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error in price_updater: {e}")
            time.sleep(10)


if __name__ == "__main__":
    updater_thread = Thread(target=price_updater, daemon=True)
    updater_thread.start()

    app.run(debug=True)
