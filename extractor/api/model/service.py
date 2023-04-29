"""Admin service."""

import uuid, os, logging
import celery
from flask import current_app
from modules.es import ES_Connector
from sqlalchemy.sql.sqltypes import INT, String

import json
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSON, TEXT, INTEGER, BOOLEAN, BYTEA
from models.map import Source, SourceField

field_types = {'TEXT': TEXT,
                'INTEGER': INTEGER,
                'BOOLEAN': BOOLEAN}

def connect_es(session, id):
    source = session.query(Source).filter_by(id = id).one()
    es_host=os.environ.get('ELASATICSEARCH_HOST')
    es_port=int(os.environ.get('ELASATICSEARCH_PORT'))
    es = ES_Connector(es_host, es_port)
    index_list = es.get_indexes_list()
    if es is not None:
        res = es.search(source.index_name, json.dumps(source.search_object))
    return res
