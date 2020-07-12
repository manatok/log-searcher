from flask_restx import Api
from flask import Blueprint

from .main.controller.auth_controller import api as auth_ns
from .main.controller.log_controller import api as log_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='Logging API',
    version='1.0',
    description='Add and query JavaScript error logs'
)

# on the /auth namespace
api.add_namespace(auth_ns)
api.add_namespace(log_ns)
