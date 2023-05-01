"""Admin service."""

import uuid, logging
import celery
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
from models.map import Source
field_types = {'TEXT': TEXT,
                'INTEGER': INTEGER,
                'BOOLEAN': BOOLEAN}

def check_table(session, table_name):
    """Проверка существования таблицы и ее создание в случае отсутствия."""
    md = MetaData()
    try:
        table = Table(str(table_name), md, autoload=True, autoload_with=session.bind.engine)
    except:
        ID_SEQ = Sequence(name = str(table_name)+'_id_serial_seq', metadata = md)
        SORT_SEQ = Sequence(name = str(table_name)+'_sort_seq', metadata = md)
        table = Table(str(table_name), md,
            Column('id_serial', INTEGER, ID_SEQ, primary_key=True, server_default = ID_SEQ.next_value()),
            Column('id', TEXT, nullable=False),
            Column('sort', INTEGER, SORT_SEQ, server_default=SORT_SEQ.next_value()),
            Column('start_version', INTEGER, nullable=True),
            Column('end_version', INTEGER, nullable=True)
        )
        md.create_all(session.bind.engine)

def create_source(session: Session, name: str, index_name: str, target_field: str, search_object: str) -> str:
    """Create object."""           
    source_id = str(uuid.uuid4())
    new_source = Source(
                id = source_id,
                name = name,
                index_name = index_name,
                target_field = target_field,
                search_object = json.loads(search_object.replace("'", '"'))
            )
    session.add(new_source)
    return source_id

def delete_source(session, key_id): 
    """Удаление временного ключа.""" 
    exists = session.query(Source).filter_by(id = key_id).first()
    if exists:
        session.query(Source).filter_by(id = key_id).delete()              

def get_all(session: Session):
    """Get objects list."""
    return session.query(Source).all()