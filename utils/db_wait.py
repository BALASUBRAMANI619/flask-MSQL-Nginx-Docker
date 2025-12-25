# utils/db_wait.py

import socket
import time
from flask import current_app
from sqlalchemy.exc import OperationalError
from extensions import db
import os


def wait_for_db():
    """
    Wait until MySQL port is accepting connections,
    then create tables safely.
    """
    uri = current_app.config['SQLALCHEMY_DATABASE_URI']

    # Extract host and port 
    host = os.getenv("DB_HOST", "db")
    port = int(os.getenv("DB_PORT", "3306"))

    retries = 30

    while retries > 0:
        try:
            with socket.create_connection((host, port), timeout=2):
                print("✅ MySQL port is open")
                break
        except OSError:
            retries -= 1
            print("⏳ Waiting for MySQL to accept connections...")
            time.sleep(2)

    if retries == 0:
        raise RuntimeError("❌ MySQL port not available")

    # Try DB connection via SQLAlchemy
    try:
        db.create_all()
        print("✅ Database tables ready")
    except OperationalError:
        raise RuntimeError("❌ Database connection failed after port opened")
