from flask import request
from flask_restx import Resource

from app.util.decorator import verified_account, \
    rate_limited, token_required, site_restricted
from ..util.dto import LogDto
from ..service.log_service import save_log, query_logs
from ..service.query_builder.tokenised_expression import TokenisationError

api = LogDto.api
log_req = LogDto.log_req
log_resp = LogDto.log_resp
error_fields = LogDto.error_fields


@api.errorhandler(TokenisationError)
@api.marshal_with(error_fields)
def handle_exception(error):
    '''This is a custom error'''
    return {'message': error.description}, error.response


@api.route('/<site_id>')
@api.param('site_id', 'The SiteID provided when registering')
class Log(Resource):
    @verified_account
    @rate_limited
    @api.expect(log_req, validate=True)
    @api.response(201, 'Log successfully stored.')
    @api.doc('save a new log record')
    def post(self, site_id):
        data = request.json
        browser = request.headers.get("User-Agent")
        url = request.values.get("url") or request.headers.get("Referer")
        ip_address = request.access_route[0] or request.remote_addr

        return save_log(data, site_id, browser, url, ip_address), 201

    @token_required
    @site_restricted
    @api.doc('query the logs')
    @api.response(code=200, model=log_resp, description='Success')
    @api.marshal_with(log_resp, envelope='data', skip_none=True)
    def get(self, site_id):
        """
        :raises TokenisationError: In case of malformed query
        """
        query = request.args.get('query')

        # pagination params
        limit = request.args.get('limit', 10)
        limit = get_int_value(limit, 10, 0)
        page = request.args.get('page', 1)
        page = get_int_value(page, 1, 1)
        offset = (page - 1) * limit

        return query_logs(query, site_id, limit, offset)


def get_int_value(value: str, default_value: int, min_allowed: int) -> int:
    try:
        value = int(value)
        if value < min_allowed:
            value = default_value
        return value
    except ValueError:
        return default_value
