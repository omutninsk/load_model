import os, random, time, uuid, datetime
from flask import Flask, request, send_file, render_template
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
from flask_migrate import Migrate

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
migrate = Migrate(app, db)

class LogItem(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.String(40), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(20))
    value = db.Column(db.String(80))

    def __repr__(self):
        return '<LogItem %r>' % self.id

class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.String(40), primary_key=True, default=uuid.uuid4)
    action = db.Column(db.String(20))
    value = db.Column(db.String(80))
    created_date = db.DateTime()

    def __repr__(self):
        return '<Setting %r>' % self.name

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
  anomaly_setting = db.session.query(Settings).filter(Settings.action == 'anomaly').first()
  anomaly = request.args.get('anomaly', False)
  if anomaly == 'on':
     anomaly_setting.value = 'true'
     db.session.commit()
  else:
     anomaly_setting.value = 'false'
     db.session.commit()
  return render_template('index_m.htm', anomaly=anomaly)

@app.route('/get_logs', methods=['GET'])
def get_logs():
  #count = int(request.args.get("count"))
  logs = LogItem.query.all()
  data = []
  for item in logs:
    data.append({"action": item.action, "value": item.value, "created_date": item.created_date})
  return {"data": data}
    

@app.route('/generate_image', methods=['GET'])  
def generate_image():
    anomaly_setting = db.session.query(Settings).filter(Settings.action == 'anomaly').first()
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
      if anomaly_setting.value == 'true':
         time.sleep(random.randint(0,5000)/1000)
      image_bytes = image.generate()
      span.add_event('End image generation.')
      span.add_event('Logging into db.')
      # item = LogItem(action="generate_image", value=f'x={x},y={y}', created_date=datetime.datetime.utcnow())
      # db.session.add(item)
      # db.session.commit()
    return send_file(image_bytes, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('SERVICE_PORT')))