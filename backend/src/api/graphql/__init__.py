from flask import Blueprint
from strawberry.flask.views import GraphQLView

from .schema import schema

graphql_bp = Blueprint("graphql", __name__)

# Configure the view with GraphiQL enabled
view = GraphQLView.as_view(
    "graphql_view",
    schema=schema,
    graphiql=True,
)
graphql_bp.add_url_rule("/graphql", view_func=view)
