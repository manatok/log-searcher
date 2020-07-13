import os


from flask import Flask, Blueprint
import redis
from flask_restx import Api

from .controller.auth_controller import api as auth_ns
from .controller.log_controller import api as log_ns
from .config import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    app.redis = redis.Redis(
        password=app.config['REDIS_PASSWORD'],
        port=app.config['REDIS_PORT'],
        host=app.config['REDIS_HOST'])

    return app


blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='Logging API',
    version='1.0',
    description='Add and query JavaScript error logs'
)

# on the /auth namespace
api.add_namespace(auth_ns, path='/auth')
# on the /log namespace
api.add_namespace(log_ns, path='/logs')

app = create_app(os.getenv('RUNNING_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()


def run():
    app.run(use_reloader=True, debug=app.config['DEBUG'])


if __name__ == '__main__':
    run()
