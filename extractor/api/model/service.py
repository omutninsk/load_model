"""Admin service."""

import uuid, os, logging
import celery
from flask import current_app
from modules.es import ES_Connector
from sqlalchemy.sql.sqltypes import INT, String
from tools.mapper import JsonMapper
import json
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSON, TEXT, INTEGER, BOOLEAN, BYTEA
from models.map import Source, SourceField

field_types = {'TEXT': TEXT,
                'INTEGER': INTEGER,
                'BOOLEAN': BOOLEAN}

def connect_es():
    es_host=os.environ.get('ELASATICSEARCH_HOST')
    es_port=int(os.environ.get('ELASATICSEARCH_PORT'))
    es = ES_Connector(es_host, es_port)
    return es

def fetch(session, id):
    source = session.query(Source).filter_by(id = id).one()
    fields = session.query(SourceField).filter_by(source_id = id).all()
    es = connect_es()
    # index_list = es.get_indexes_list()
    if es is not None:
        res = es.search(source.index_name, json.dumps(source.search_object))

    source = res.get('hits').get('hits')[0].get('_source')

    target = {}

    for field in fields:
        mapper = JsonMapper(source=source, target=target, rules=field.operations)
        mapper.run()
    return target, source

def get_mapped_data(session, id):
    source = session.query(Source).filter_by(id = id).one().one()
    
    
    
