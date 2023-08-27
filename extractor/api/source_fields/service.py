"""Admin service."""

import uuid, logging
import re
from flask import current_app
from sqlalchemy.sql.sqltypes import INT, String

import json
from datetime import datetime
import pandas as pd
from sqlalchemy import MetaData, Table, Column, Sequence
from sqlalchemy.orm import subqueryload, with_expression
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSON, TEXT, INTEGER, BOOLEAN, BYTEA
from models.map import SourceField
field_types = {'TEXT': TEXT,
                'INTEGER': INTEGER,
                'BOOLEAN': BOOLEAN}

def create_source_field(session: Session, name: str, source_id: str, operations: str, variable_type: str) -> str:
    """Create object."""           
    source_field_id = str(uuid.uuid4())
    operations = operations.replace("'", '"')
    new_source = SourceField(
                id = source_field_id,
                name = name,
                source_id = source_id,
                operations = json.loads(operations),
                variable_type = variable_type
            )
    session.add(new_source)
    return source_id

def delete_source_field(session, id): 
    """Удаление поля данных.""" 
    exists = session.query(SourceField).filter_by(id = id).first()
    if exists:
        session.query(SourceField).filter_by(id = id).delete()              

def get_source_fields_by_source_id(session, id): 
    """Получение полей данных по родительскому ид."""
    if id == None:
        return session.query(SourceField).all()
    else:
        return session.query(SourceField).filter_by(source_id = id).all()
    

def get_all(session: Session):
    """Get objects list."""
    return session.query(SourceField).all()