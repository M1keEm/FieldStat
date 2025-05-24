import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    load_dotenv()
    from .config import Config

    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object('backendFlask.config.Config')
    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.main import main_bp
    from .routes.weather import weather_bp
    from .routes.plot import plot_bp
    from .routes.auth import auth_bp
    from .routes.protected import protected_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(plot_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(protected_bp)

    from . import models  # Ensure models are loaded

    return app
