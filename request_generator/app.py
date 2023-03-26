import os, requests, time
from flask import Flask, render_template, request
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentracing.propagation import Format
from celery import Celery


name=os.environ.get('SERVICE_NAME')

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
  TracerProvider(
    resource=Resource.create({SERVICE_NAME: name})
  )
)
jaeger_exporter = JaegerExporter(
  agent_host_name=os.environ.get('AGENT_HOST_NAME'),
  agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(name)

app = Flask(name)
celery = Celery(app.name, broker='amqp://rabbit_user:rabbit_password@localhost:5672//')

@celery.task
def send_requests(url, requests_per_second):
    while True:
        for i in range(requests_per_second):
            requests.get(url)
        time.sleep(1)

def make_requests(endpoint1_requests, endpoint2_requests):
    send_requests.delay('http://endpoint1.com', endpoint1_requests)
    send_requests.delay('http://endpoint2.com', endpoint2_requests)

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
 
app.run(host='0.0.0.0', port=8000)