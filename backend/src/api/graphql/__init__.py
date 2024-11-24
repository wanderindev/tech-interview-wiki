from flask import Blueprint
from strawberry.flask.views import GraphQLView

from .schema import schema

graphql_bp = Blueprint("graphql", __name__)

view = GraphQLView.as_view("graphql_view", schema=schema)
graphql_bp.add_url_rule("/graphql", view_func=view)
