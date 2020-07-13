from flask import request
from flask_restx import Resource
from werkzeug.exceptions import BadRequest

from app.util.decorator import verified_request, \
    rate_limited_request, token_required
from ..util.dto import LogDto
from ..service.log_service import save_log, query_logs
from ..service.exception import TokenisationError, RateLimitExceededError

api = LogDto.api
log_req = LogDto.log_req
log_resp = LogDto.log_resp
error_fields = LogDto.error_fields


@api.errorhandler(TokenisationError)
@api.errorhandler(RateLimitExceededError)
@api.marshal_with(error_fields)
@api.header('My-Header',  'Some description')
def handle_exception(error):
    '''This is a custom error'''
    return {'message': error.description}, error.response, {'My-Header': 'Value'}


@api.route('/<site_id>')
@api.param('site_id', 'The SiteID provided when registering')
class Log(Resource):
    @verified_request
    @rate_limited_request
    @api.expect(log_req, validate=True)
    @api.response(201, 'Log successfully stored.')
    @api.doc('save a new log record')
    def post(self, site_id):
        data = request.json
        browser = request.headers.get("User-Agent")
        url = request.values.get("url") or request.headers.get("Referer")
        ip_address = request.access_route[0] or request.remote_addr

        return save_log(data, site_id, browser, url, ip_address)

    @token_required
    @api.doc('query the logs')
    @api.response(code=200, model=log_resp, description='Success')
    # @api.response(code=400, model=log_resp, description='Invalid Query')
    # @api.marshal_with(log_resp, envelope='data', skip_none=True)
    def get(self, site_id):
        """
        :raises TokenisationError: In case of malformed query
        """
        query = request.args.get('query')
        return query_logs(query, site_id)
