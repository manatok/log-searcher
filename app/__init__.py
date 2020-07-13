import redis
from flask import Flask
from werkzeug.exceptions import HTTPException
from .config import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    app.redis = redis.Redis(
        password=app.config['REDIS_PASSWORD'],
        port=app.config['REDIS_PORT'],
        host=app.config['REDIS_HOST'])

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return {
            'message': "An error occurred while serving the request!"
        }, code

    return app
