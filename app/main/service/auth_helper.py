from app.main.model.user import User


class Auth:

    @staticmethod
    def login_user(data):
        try:
            user = User.get_by_email(data.get('email'))

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
