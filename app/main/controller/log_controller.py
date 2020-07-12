from flask import request
from flask_restx import Resource

from app.main.util.decorator import verified_request, rate_limited_request
from ..util.dto import LogDto
from ..service.log_service import save_log

api = LogDto.api
log_req = LogDto.log_req


@api.route('/<site_id>')
@api.param('site_id', 'Site ID received when registering')
@api.response(404, 'Site not found.')
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
