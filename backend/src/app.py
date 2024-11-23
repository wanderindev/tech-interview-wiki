import os

from flask import Flask

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

    return app
