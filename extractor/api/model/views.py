"""Admin views."""

import uuid, datetime, os, math, shutil, json
from flask import Blueprint, request, send_from_directory, current_app
from flask.views import MethodView
from sqlalchemy.orm import session
from sqlalchemy.sql import select, desc

from . import service as model_service
from models import schema as base_schemas
from tools.flasgger_marshmallow import swagger_decorator
from session import session_scope

model_blueprint = Blueprint('model', __name__)


class Fetch(MethodView):
    @swagger_decorator(query_schema=base_schemas.GetByIdQuerySchema, response_schema={400: base_schemas.ErrorResponseSchema})
    def get(self):
        """Обработка логов."""
        id= request.query_schema["id"]
        with session_scope() as session:
            res = model_service.connect_es(session, id)
            return {"data": res}

model_blueprint.add_url_rule('/fetch/', view_func=Fetch.as_view("fetch_api"))
