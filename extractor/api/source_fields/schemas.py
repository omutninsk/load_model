"""Query and response schemas."""

from marshmallow import fields, EXCLUDE, INCLUDE
from flask_marshmallow import Schema


class SourceFieldCreateCommandSchema(Schema):
    """Команда создания источника данных."""

    name = fields.String(required=True, doc='Название')
    operations = fields.String(required=True, doc='Обработчики поля')
    variable_type = fields.String(required=True, doc='Тип переменной')
    source_id = fields.String(required=True, doc='Идентификатор источника данных')
    class Meta:
        """Meta."""

        strict = True
        unknown = EXCLUDE

class SourceFieldResponseSchema(Schema):
    """Sources list."""
    id = fields.String(required=True, doc='id')
    name = fields.String(required=True, doc='Название')
    operations = fields.String(required=True, doc='Обработчики поля')
    variable_type = fields.String(required=True, doc='Тип переменной')
    source_id = fields.String(required=True, doc='Идентификатор источника данных')
    class Meta:
        """Meta."""

        strict = True
        unknown = EXCLUDE

class SourceFieldListResponseSchema(Schema):
    """Список объектов."""

    class Meta:
        """Meta."""

        strict = True
        unknown = EXCLUDE

    items = fields.Nested(SourceFieldResponseSchema, many=True, doc='Список источников данных')
