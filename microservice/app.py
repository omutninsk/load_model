import os, random, time
from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


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

FlaskInstrumentor().instrument_app(app)


@app.route('/')
def index():
  with tracer.start_as_current_span("server_request") as span:
    span.add_event('Start processing request.')
    time.sleep(random.randint(0,2000)/1000)
    span.add_event('End processing request.')
    return 'Hello World!'
    
 
app.run(host='0.0.0.0', port=int(os.environ.get('SERVICE_PORT')))