from flask import Flask
from config import config
from . import errors


def create_app(config_name):
    """Factory function to create an instance of the flask application"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_v1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0/')

    return app
