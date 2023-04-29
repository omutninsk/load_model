"""Admin views."""

import uuid, datetime, os, math, shutil, json
from flask import Blueprint, request, send_from_directory, current_app
from flask.views import MethodView
from sqlalchemy.orm import session
from sqlalchemy.sql import select, desc

from . import service as source_service
from . import schemas as source_schemas
from models import schema as base_schemas
from tools.flasgger_marshmallow import swagger_decorator
from session import session_scope

sources_blueprint = Blueprint('sources', __name__)


class Source(MethodView):
    """Source."""

    @swagger_decorator(form_schema=source_schemas.SourceCreateCommandSchema, response_schema={200: base_schemas.SuccessResponseSchema, 400: base_schemas.ErrorResponseSchema})
    def post(self):
        """Создание источника данных."""
        index_name = request.form_schema["index_name"]
        name = request.form_schema["name"]
        target_field = request.form_schema["target_field"]
        search_object = request.form_schema["search_object"]
        with session_scope() as session:
            id = source_service.create_source(session, name, index_name, target_field, search_object)
        return {"msg": "Объект создан", "data": {"id": id}}
    
    @swagger_decorator(query_schema=base_schemas.GetByIdQuerySchema, response_schema={200: base_schemas.SuccessResponseSchema, 400: base_schemas.ErrorResponseSchema})
    def delete(self):
        """Удаление источника данных."""
        id = request.query_schema["id"]
        with session_scope() as session:
            source_service.delete_source(session, id)
            return {"data":{"sucsess": True}}

class SourcesList(MethodView):
    """Sources list."""

    @swagger_decorator(response_schema={200: source_schemas.SourceListResponseSchema, 400: base_schemas.ErrorResponseSchema})
    def get(self):
        """Список объектов."""
        with session_scope() as session:
            items = source_service.get_all(session)
            result = source_schemas.SourceResponseSchema(many=True).dump(items)     
        return {"items": result}

sources_blueprint.add_url_rule('/', view_func=Source.as_view("source_api"))
sources_blueprint.add_url_rule('/list/', view_func=SourcesList.as_view("sources_list_api"))