from flask_restx import Namespace, fields


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password'),
    })

    error_fields = api.model('error_fields', {
        'message': fields.String(required=True, description='The error message')
    })

    auth_success = api.model('auth_success', {
        'Authorization': fields.String(required=True, description='The Auth token')
    })


class LogDto:
    api = Namespace('logs', description='logging related operations')

    log_req = api.model('log_req', {
        'message': fields.String(required=True, description='The error log message')
    })

    log_resp = api.model('log_resp', {
        'message': fields.String(required=True, description='The error log message'),
        'browser': fields.String(required=False, description='The browser of the user'),
        'url': fields.String(required=False, description='The URL the error occurred on'),
        'country': fields.String(required=False, description='The country the user is from'),
    })

    error_fields = api.model('error_fields', {
        'message': fields.String(required=True, description='The error message')
    })
