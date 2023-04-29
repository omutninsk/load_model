"""Query and response schemas."""

from marshmallow import fields, EXCLUDE, INCLUDE
from flask_marshmallow import Schema


class SourceCreateCommandSchema(Schema):
    """Команда создания источника данных."""

    name = fields.String(required=True, doc='Название')
    index_name = fields.String(required=True, doc='Индекс ElasticSearch в котором идет поиск')
    target_field = fields.String(required=True, doc='Поле, в котором находится целевое значение')
    search_object = fields.String(required=True, doc='Объект поиска')
    class Meta:
        """Meta."""

        strict = True
        unknown = EXCLUDE

class SourceResponseSchema(Schema):
    """Sources list."""
    id = fields.String(required=True, doc='id')
    name = fields.String(required=True, doc='Название')
    index_name = fields.String(required=True, doc='Индекс ElasticSearch в котором идет поиск')
    target_field = fields.String(required=True, doc='Поле, в котором находится целевое значение')
    search_object = fields.String(required=True, doc='Объект поиска')
    class Meta:
        """Meta."""

        strict = True
        unknown = EXCLUDE

class SourceListResponseSchema(Schema):
    """Список объектов."""

    class Meta:
        """Meta."""

        strict = True
        unknown = EXCLUDE

    items = fields.Nested(SourceResponseSchema, many=True, doc='Список источников данных')
