from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from config import config

# TODO: remove flask-bootstrap and flask-moments and use standard
#       implementations
bootstrap = Bootstrap()
moment = Moment()


def create_app(config_name):
    """Factory function to create an instance of the flask application"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
