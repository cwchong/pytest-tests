from flask_restx import Namespace, fields


'''Data transfer object for moving data b/w processes'''
class UserDto:
    api = Namespace('user', description='user stuff')
    user = api.model('user', {
        'email': fields.String(required=True, description='email address'),
        'username': fields.String(required=True, description='username'),
        'password': fields.String(required=True, description='password'),
        'public_id': fields.String(description='user id'),

    })