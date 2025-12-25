# app.py

from flask import Flask
from config import Config
from extensions import db
from auth.routes import auth
from main.routes import main
from utils.db_wait import wait_for_db
from werkzeug.middleware.proxy_fix import ProxyFix
import pymysql

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    db.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(main)

    with app.app_context():
        wait_for_db()   # 👈 MySQL wait happens here

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
