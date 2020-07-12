from flask import Flask
from .config import config_by_name
from elasticsearch import Elasticsearch
import redis


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    app.es = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    app.redis = redis.Redis(
        password=app.config['REDIS_PASSWORD'],
        port=app.config['REDIS_PORT'],
        host=app.config['REDIS_HOST'])

    return app
