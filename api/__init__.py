from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/todo/api/v1.0')

    if app.config['USE_TOKEN_AUTH']:
        from .api_1_0.token import token as token_blueprint
        app.register_blueprint(token_blueprint, url_prefix='/auth')

    return app

