import os

class Config:
    DB_USER = os.getenv("USERNAME")
    DB_PASS = os.getenv("PASSWORD")
    DB_HOST = "db"  # Use service name for Docker
    DB_PORT = os.getenv("DATABASE_PORT")
    DB_NAME = os.getenv("DATABASE_NAME").replace('"', '')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")