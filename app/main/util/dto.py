from flask_restx import Namespace, fields
'''Data transfer objects for moving data b/w processes'''


class UserDto:
    api = Namespace('user', description='user stuff')
    user = api.model('user', {
        'email': fields.String(required=True, description='email address'),
        'username': fields.String(required=True, description='username'),
        'password': fields.String(required=True, description='password'),
        'public_id': fields.String(description='user id'),

    })


class AuthDto:
    api = Namespace('auth', description='auth stuff')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='email'),
        'password': fields.String(required=True, description='password')
    })