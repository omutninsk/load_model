import os, random, time, uuid, datetime
from flask import Flask, request, send_file
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from flask_sqlalchemy import SQLAlchemy

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
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
class LogItem(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.String(40), primary_key=True, default=uuid.uuid4)
    action = db.Column(db.String(20), unique=True)
    value = db.Column(db.String(80), unique=True)
    created_date = db.DateTime()

    def __init__(self, username, email):
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username

FlaskInstrumentor().instrument_app(app)


from randimage import get_random_image
import matplotlib, io

class RandomImage():
    def __init__(self, x,y):
        self.x = x
        self.y = y
    
    def generate(self):
        img_size = (self.x,self.y)
        img = get_random_image(img_size)
        image_bytes = io.BytesIO()
        matplotlib.image.imsave(image_bytes, img)
        image_bytes.seek(0)
        return image_bytes

@app.route('/')
def index():
  with tracer.start_as_current_span("server_request") as span:
    span.add_event('Start processing request.')
    time.sleep(random.randint(0,2000)/1000)
    span.add_event('End processing request.')
    return 'Hello World!'

@app.route('/generate_image', methods=['GET'])  
def generate_image():
    x = int(request.args.get("x"))
    y = int(request.args.get("y"))
    additional = request.args.get("additional", None)
    if additional == "one":
       x += 100
       y += 100
    elif additional == "two":
       x += 200
       y += 200
    elif additional == "three":
       x += 300
       y += 300
    elif additional == "four":
       x += 400
       y += 150
    else:
       pass
    
    with tracer.start_as_current_span("image_generator") as span:
      span.add_event('Start processing request.')
      image = RandomImage(x,y)
      span.add_event('Start image generation.')
      image_bytes = image.generate()
      span.add_event('End image generation.')
      span.add_event('Logging into db.')
      item = LogItem(action="generate_image", value=f'x={x},y={y}', created_date=datetime.datetime.utcnow())
      db.session.add(item)
      db.session.commit()
    return send_file(image_bytes, mimetype='image/jpeg')

if __name__ == '__main__':
    with app.app_context():
        print("create db if not exists")
        db.metadata.create_all(bind='__all__')
    app.run(host='0.0.0.0', port=int(os.environ.get('SERVICE_PORT')))