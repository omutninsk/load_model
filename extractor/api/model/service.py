"""Admin service."""

import uuid, os, logging
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import numpy as np
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

def encode_column(column_name, dataset):
    column_data = dataset[column_name].values.reshape(-1, 1)
    encoder = OneHotEncoder()
    encoded_data = encoder.fit_transform(column_data).toarray()
    categories = encoder.categories_[0]
    encoded_df = pd.DataFrame(encoded_data, columns=[f'{column_name}_{cat}' for cat in categories])
    dataset.drop([column_name], axis=1, inplace=True)
    return pd.concat([dataset, encoded_df], axis=1)

def add_parallel_processes(data):
    
    #data['duration'] = data['duration'].astype(np.int64)
    #data['starttime'] = data['starttime'].astype(np.int64)

    # Создание столбцов start и end
    data['start'] = data['starttime']
    data['end'] = data['start'] + data['duration']

    # Создание столбца parallel_processes
    parallel_processes = []
    for i in range(len(data)):
        start = data.iloc[i]['start']
        end = data.iloc[i]['end']
        parallel = len(data[(data['start'] <= start) & (data['end'] > start) | (data['start'] < end) & (data['end'] >= end)])
        parallel_processes.append(parallel)
    data['parallel_processes'] = parallel_processes
    data.drop(['start', 'end'], axis=1, inplace=True)
    return data

def connect_es():
    es_host=os.environ.get('ELASATICSEARCH_HOST')
    es_port=int(os.environ.get('ELASATICSEARCH_PORT'))
    es = ES_Connector(es_host, es_port)
    return es

def fetch(session, id, count):
    source = session.query(Source).filter_by(id = id).one()
    fields = session.query(SourceField).filter_by(source_id = id).all()
    es = connect_es()
    # index_list = es.get_indexes_list()
    if es is not None:
        res = es.search(source.index_name, json.dumps(source.search_object), count)

    source = res.get('hits').get('hits')[0]
    result = {}
    for field in fields:
        target = {}
        mapper = JsonMapper(source=source, target=target, rules=field.operations)
        res = mapper.run()
        result.update(res)
    
    return result, source

def fit(session, id, count):
    result = []
    source = session.query(Source).filter_by(id = id).one()
    fields = session.query(SourceField).filter_by(source_id = id).all()
    es = connect_es()
    if es is not None:
        res = es.search(source.index_name, json.dumps(source.search_object), count)
    source = res.get('hits').get('hits')

    for item in source:
        record = {}
        for field in fields:
            target = {}
            mapper = JsonMapper(source=item, target=target, rules=field.operations)
            res = mapper.run()
            record.update(res)
        result.append(record)
    return result

def get_mapped_data(session, id):
    source = session.query(Source).filter_by(id = id).one().one()
    
    
    
