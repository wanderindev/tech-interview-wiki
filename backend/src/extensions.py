from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
redis_client = Redis()
