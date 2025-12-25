# config.py
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://"
        f"{os.getenv('DB_USER', 'root')}:"
        f"{os.getenv('DB_PASSWORD', 'password')}"
        f"@{os.getenv('DB_HOST', 'db')}:"
        f"{os.getenv('DB_PORT', '3306')}/"
        f"{os.getenv('DB_NAME', 'flask_auth')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
