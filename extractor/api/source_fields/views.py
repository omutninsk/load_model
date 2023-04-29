"""Admin views."""

import uuid, datetime, os, math, shutil, json
from flask import Blueprint, request, send_from_directory, current_app
from flask.views import MethodView
from sqlalchemy.orm import session
from sqlalchemy.sql import select, desc

from . import service as source_field_service
from . import schemas as source_field_schemas
from models import schema as base_schemas
from tools.flasgger_marshmallow import swagger_decorator
from session import session_scope

source_fields_blueprint = Blueprint('source_fields', __name__)


class SourceField(MethodView):
    """Source Fields."""

    @swagger_decorator(form_schema=source_field_schemas.SourceFieldCreateCommandSchema, response_schema={200: base_schemas.SuccessResponseSchema, 400: base_schemas.ErrorResponseSchema})
    def post(self):
        """Добавление поля источника данных."""
        name = request.form_schema["name"]
        source_id = request.form_schema["source_id"]
        operations = request.form_schema["operations"]
        with session_scope() as session:
            id = source_field_service.create_source_field(session, name, source_id, operations)
        return {"msg": "Объект создан", "data": {"id": id}}
    
    @swagger_decorator(query_schema=base_schemas.GetByIdQuerySchema, response_schema={200: source_field_schemas.SourceFieldListResponseSchema, 400: base_schemas.ErrorResponseSchema})
    def get(self):
        """Получение полей источника данных по идентификатору"""
        id = request.query_schema["id"]
        with session_scope() as session:
            items = source_field_service.get_source_fields_by_source_id(session, id)
            result = source_field_schemas.SourceFieldResponseSchema(many=True).dump(items)     
        return {"items": result}
    
    @swagger_decorator(query_schema=base_schemas.GetByIdQuerySchema, response_schema={200: base_schemas.SuccessResponseSchema, 400: base_schemas.ErrorResponseSchema})
    def delete(self):
        """Удаление поля источника данных."""
        id = request.query_schema["id"]
        with session_scope() as session:
            source_field_service.delete_source_field(session, id)
            return {"data":{"sucsess": True}}

class SourceFieldsList(MethodView):
    """Sources list."""

    @swagger_decorator(response_schema={200: source_field_schemas.SourceFieldListResponseSchema, 400: base_schemas.ErrorResponseSchema})
    def get(self):
        """Список полей данных."""
        with session_scope() as session:
            items = source_field_service.get_all(session)
            result = source_field_schemas.SourceFieldResponseSchema(many=True).dump(items)     
        return {"items": result}

source_fields_blueprint.add_url_rule('/', view_func=SourceField.as_view("source_field_api"))
source_fields_blueprint.add_url_rule('/list/', view_func=SourceFieldsList.as_view("source_fields_list_api"))