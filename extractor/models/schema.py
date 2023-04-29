"""Schemas."""

#region imports

from marshmallow import fields, EXCLUDE, INCLUDE
from flask_marshmallow import Schema

#endregion


class SuccessResponseSchema(Schema):
    """Ответ при успешном выполнении запроса."""

    class Meta:
        """Meta."""

        strict = True

    msg = fields.String(doc='Сообщение')
    data = fields.Dict(doc='Данные')

class ErrorItemResponseSchema(Schema):
    """Ошибка запроса."""

    class Meta:
        """Meta."""

        strict = True

    id = fields.String(doc='Идентификатор')
    msg = fields.String(doc='Сообщение')
    detail = fields.String(doc='Описание')

class GetByIdQuerySchema(Schema):
    """Запрос получения данных."""

    id = fields.String(required=True, doc='Идентификатор')

    class Meta:
        """Meta."""

        strict = True


class ErrorResponseSchema(Schema):
    """Ответ при неправильном выполнении запроса."""

    class Meta:
        """Meta."""

        strict = True

    msg = fields.String(doc='Сообщение')
    errors = fields.Nested(ErrorItemResponseSchema, many=True, doc='Ошибки')
