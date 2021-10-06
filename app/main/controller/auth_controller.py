from flask import request
from flask_restx import Resource

from ..util.dto import AuthDto
from ..service.auth_helper import Auth

api = AuthDto.api
_user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    @api.doc('user login')
    @api.expect(_user_auth, validate=True)
    def post(self):
        post_data = request.get_json()
        return Auth.login_user(data=post_data)


@api.route('/logout')
class UserLogout(Resource):
    @api.doc('logout user')
    def post(self):
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)