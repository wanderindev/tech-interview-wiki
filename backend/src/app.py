import os

from flask import Flask

from cli import populate_db_command
from config import config
from extensions import db, migrate, jwt, cors, redis_client


def create_app(config_name=None):
    """Application factory function"""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    redis_client.from_url(app.config["REDIS_URL"])

    # Register blueprints
    from api.articles import articles_bp

    app.register_blueprint(articles_bp, url_prefix="/api/articles")

    # Register CLI commands
    app.cli.add_command(populate_db_command)

    # Configure logging
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(
            "logs/app.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Application startup")

    return app
