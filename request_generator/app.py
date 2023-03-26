import os, time, requests
from flask import Flask, jsonify, request, render_template
from celery import Celery, Task
from celery import shared_task
#from flower import Flower
from celery.signals import worker_process_init
from opentelemetry import trace
#from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
#from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


name=os.environ.get('SERVICE_NAME')

@worker_process_init.connect(weak=False)
def init_celery_tracing(*args, **kwargs):
    trace.set_tracer_provider(TracerProvider(
        resource=Resource.create({SERVICE_NAME: name})
    ))
    exporter = OTLPSpanExporter(
        endpoint="http://microservice1:5011",
        insecure=True,
    )
    span_processor = BatchSpanProcessor(exporter)
    #span_processor = BatchSpanProcessor(ConsoleSpanExporter())
    trace.get_tracer_provider().add_span_processor(span_processor)
    
    CeleryInstrumentor().instrument()

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app = Flask(name)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
celery_broker = os.environ.get('CELERY_BROKER')
celery_backend = os.environ.get('CELERY_BACKEND')

app.config.from_mapping(
    CELERY=dict(
        broker_url=celery_broker,
        result_backend=celery_backend,
        task_ignore_result=True,
    ),
)
celery = celery_init_app(app)

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

@celery.task(ignore_result=False)
def send_requests(url, requests_per_second):
    with trace.get_tracer(__name__).start_as_current_span('send_request to microsrvice') as span:
        while True:
            for i in range(requests_per_second):
                with tracer.start_as_current_span('make_request') as request_span:
                    span.add_event(f'Send request {url}')
                    requests.get(url)
            time.sleep(1)

def make_requests(endpoint1_requests, endpoint2_requests):
    with tracer.start_as_current_span('make_requests') as span:
        span.add_event('Start tasks')
        send_requests.delay('http://microservice1:5011', endpoint1_requests)
        send_requests.delay('http://microservice2:5012', endpoint2_requests)

def make_sync_request(url, requests_per_second):
    for i in range(requests_per_second):
        with tracer.start_as_current_span('make_request') as span:
            span.add_event(f'Send request {url}')
            requests.get(url)

@app.route('/')
def index():
  with tracer.start_as_current_span("server_request") as span:
    endpoint1_requests = int(request.args.get('endpoint1', 1))
    endpoint2_requests = int(request.args.get('endpoint2', 2))
    try:
        span.add_event('Start request generation')
        # headers = {}
        # make_requests(endpoint1_requests, endpoint2_requests)
        make_sync_request('http://localhost:5011', endpoint1_requests)
        make_sync_request('http://localhost:5012', endpoint2_requests)
    except Exception as e:
       span.add_event(f'Error while generating requests: {str(e)}')
    return render_template('index.html', endpoint1=endpoint1_requests, endpoint2=endpoint2_requests)

if __name__ == "__main__": 
  app.run(host='0.0.0.0', port=8000)