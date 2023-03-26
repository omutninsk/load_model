import os, requests, time
from flask import Flask, render_template, request
from flask_opentracing import FlaskTracing
from opentracing.scope_managers.contextvars import ContextVarsScopeManager
from opentracing import Tracer, Format

from celery import Celery
from celery.signals import task_prerun, task_postrun

import requests
import time

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://rabbit_user:rabbit_password@localhost:5672//'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://rabbit_user:rabbit_password@localhost:5672//'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

tracer = Tracer(
    os.environ.get('SERVICE_NAME'),
    scope_manager=ContextVarsScopeManager(),
    # configure tracer to use Jaeger
)

FlaskTracing(tracer, True, app)

@task_prerun.connect
def before_task_execution(sender, task_id, task, *args, **kwargs):
    parent_span = tracer.extract(Format.HTTP_HEADERS, task.request.headers)
    task_span = tracer.start_span(task.name, child_of=parent_span)
    task_span.set_tag('task_id', task_id)
    setattr(task.request, 'task_span', task_span)

@task_postrun.connect
def after_task_execution(sender, task_id, task, retval, *args, **kwargs):
    task_span = getattr(task.request, 'task_span', None)
    if task_span:
        task_span.finish()

@celery.task
def send_requests(url, requests_per_second, parent_span):
    with tracer.start_active_span('send_requests', child_of=parent_span) as span:
        while True:
            for i in range(requests_per_second):
                with tracer.start_active_span('make_request', child_of=span) as request_span:
                    requests.get(url)
            time.sleep(1)

def make_requests(endpoint1_requests, endpoint2_requests):
    with tracer.start_active_span('make_requests') as span:
        parent_span = span.span_context
        send_requests.delay('http://localhost:5011', endpoint1_requests, parent_span)
        send_requests.delay('http://localhost:5012', endpoint2_requests, parent_span)

@app.route('/')
def index():
  with tracer.start_as_current_span("server_request") as span:
    endpoint1_requests = int(request.args.get('endpoint1', 1))
    endpoint2_requests = int(request.args.get('endpoint2', 2))
    try:
        span.add_event('Start request generation')
        headers = {}
        make_requests(endpoint1_requests, endpoint2_requests)
        span.add_event('End request generation')
    except Exception as e:
       span.add_event(f'Error while generating requests: {str(e)}')
    return render_template('index.html', endpoint1=endpoint1_requests, endpoint2=endpoint2_requests)

if __name__ == '__main__':
    celery.worker_main(['worker', '--loglevel=INFO', '-Ofair'])
    app.run(debug=True, host='0.0.0.0')