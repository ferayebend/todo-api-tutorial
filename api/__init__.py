import os

from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

from celery import Celery

db = SQLAlchemy()
celery = Celery(__name__,
                broker=os.environ.get('CELERY_BROKER_URL', 'redis://'),
                backend=os.environ.get('CELERY_BROKER_URL', 'redis://'))


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    celery.conf.update(config[config_name].CELERY_CONFIG)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/todo/api/v1.0')

    if app.config['USE_TOKEN_AUTH']:
        from .api_1_0.token import token as token_blueprint
        app.register_blueprint(token_blueprint, url_prefix='/auth')

    from .api_1_0.ctasks import ctasks_bp as ctasks_blueprint
    app.register_blueprint(ctasks_blueprint, url_prefix='/ctasks')

    return app
