import os, random, time, uuid, datetime, json
from flask import Flask, request, send_file, render_template
from modules.es import ES_Connector
from flask import Flask, send_from_directory
from celery import Celery
from sqlalchemy import create_engine
from flasgger import Swagger
from flask_marshmallow import Marshmallow
from models.map import Base
from api import blueprints
import sys, traceback


def internal_server_error(e):
    traceback.print_exc()
    return 'Ой...', 500


def get_app(config) -> Flask:
    """Get flask application."""
    name=os.environ.get('SERVICE_NAME')
    app = Flask(name)
    app.config.from_object(config)

    # @app.route('/')
    # def index():
    #     return {"res": res}

    # @app.route('/assets/js/<path:path>')
    # def send_js(path):
    #     return send_from_directory('templates/assets/js/', path)
    
    # @app.route('/assets/css/<path:path>')
    # def send_css(path):
    #     return send_from_directory('templates/assets/css/', path)

    # @app.route('/assets/fonts/<path:path>')
    # def send_fonts(path):
    #     return send_from_directory('templates/assets/fonts/', path)

    # @app.route('/assets/img/<path:path>')
    # def send_img(path):
    #     return send_from_directory('templates/assets/img/', path)
    
    # @app.route('/assets/favicon.ico')
    # def send_favicon():
    #     return send_from_directory('templates/assets/', 'favicon.ico')


    Marshmallow(app)
    Swagger(app) 
    for blueprint in blueprints:
        app.register_blueprint(blueprint.obj, url_prefix = blueprint.url_prefix)
    app.register_error_handler(Exception, internal_server_error)
    engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI', ''))
    Base.metadata.create_all(engine)
    return app

