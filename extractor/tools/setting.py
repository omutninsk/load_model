"""Settings."""

import os
from flask import current_app


class BaseConfig(object):
    """Base configuration."""

    DEBUG = False
    SECRET_KEY = "MY_VERY_SECRET_KEY"
    CSRF_ENABLED = True
    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    PROPAGATE_EXCEPTIONS = True
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND")
    UPLOAD_FOLDER = os.path.join(ROOT_PATH, "uploads")
    DOWNLOAD_FOLDER = os.path.join(ROOT_PATH, "downloads")
