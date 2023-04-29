"""Views."""

from flask import Blueprint
from flask.views import MethodView
from sqlalchemy.sql import func, select

from . import schemas as user_schemas
from models import schema as base_schemas
from tools.flasgger_marshmallow import swagger_decorator
from session import session_scope


user_blueprint = Blueprint('user', __name__)


class UserCurrentGet(MethodView):
    """Get user current."""

    @swagger_decorator(response_schema={200: user_schemas.UserResponseSchema, 400: base_schemas.ErrorResponseSchema})
    def get(self):
        """Получение информации о текущем пользователе."""
        name = "user"
        return {"name": name}


user_blueprint.add_url_rule('/current', view_func=UserCurrentGet.as_view("user_current_api"))
