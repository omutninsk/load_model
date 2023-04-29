import os, random, time, uuid, datetime, json
from flask import Flask, request, send_file, render_template
from modules.es import ES_Connector

name=os.environ.get('SERVICE_NAME')
es_host=os.environ.get('ELASATICSEARCH_HOST')
es_port=int(os.environ.get('ELASATICSEARCH_PORT'))
app = Flask(name)

@app.route('/')
def index():
    es = ES_Connector(es_host, es_port)
    index_list = es.get_indexes_list()
    if es is not None:
        search_object = {'query': {'match': {'process.serviceName': 'microservice1'}}}
        res = es.search('jaeger-*', json.dumps(search_object))
    return {"res": res}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('SERVICE_PORT')))

