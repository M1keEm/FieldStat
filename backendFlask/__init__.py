import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()
    from .config import Config

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.main import main_bp
    from .routes.weather import weather_bp
    from .routes.plot import plot_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(plot_bp)

    from . import models  # Ensure models are loaded

    return app