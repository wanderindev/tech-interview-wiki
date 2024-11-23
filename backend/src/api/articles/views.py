from flask import jsonify

from . import articles_bp
from .models import Article


@articles_bp.route("/", methods=["GET"])
def get_articles():
    return jsonify({"status": "success", "message": "Articles endpoint", "data": []})
