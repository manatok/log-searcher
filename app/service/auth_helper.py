import jwt
from app.model.user import User
from app.model.site import Site
from urllib.parse import urlparse


class Auth:

    @staticmethod
    def login_user(data):
        try:
            user = User.get_by('email', data.get('email'))

            if user and user.check_password(data.get('password')):
                auth_token = user.encode_auth_token()
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401

        except Exception:
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def get_logged_in_user(new_request):

        auth_token = new_request.headers.get('Authorization')

        if auth_token:
            try:
                resp = User.decode_auth_token(auth_token)
            except jwt.ExpiredSignatureError:
                return {
                    'status': 'fail',
                    'message': 'Signature expired. Please log in again.'
                }, 401
            except jwt.InvalidTokenError:
                return {
                    'status': 'fail',
                    'message': 'Invalid token. Please log in again.'
                }, 401

            user = User.get_by('id', resp['id'])
            response_object = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'email': user.email,
                    'allowed_site_ids': user.allowed_site_ids
                }
            }
            return response_object, 200

        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401

    @staticmethod
    def verify_request(new_request, site_id):

        referrer = new_request.headers.get("Referer")

        if not referrer:
            response_object = {
                'status': 'fail',
                'message': 'Referer HTTP header not set'
            }
            return response_object, 401

        site = Site.get_by_id(site_id)

        if site:
            parsed_uri = urlparse(referrer)

            if parsed_uri.scheme == site.scheme and \
                    parsed_uri.netloc == site.domain:

                response_object = {
                    'status': 'success',
                    'data': {
                        'id': site.id,
                        'max_requests': site.max_requests,
                        'window_seconds': site.window_seconds
                    }
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'SiteId not registered for this domain'
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Site not found'
            }
            return response_object, 401
