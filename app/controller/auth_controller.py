from flask import request
from flask_restx import Resource

from app.service.authentication import login_user
from ..util.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth
auth_success = AuthDto.auth_success


@api.route('/login')
class UserLogin(Resource):
    """
     User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    @api.marshal_with(auth_success)
    def post(self):
        post_data = request.json
        return {
            'Authorization': login_user(
                email=post_data.get('email'),
                password=post_data.get('password')
            )
        }
