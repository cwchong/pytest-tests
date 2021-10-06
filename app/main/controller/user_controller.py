from flask import request
from flask_restx import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_one_user

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list of users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        '''
        marshal is for controlling actual output
        expect is for swagger docs, similarly for api.response
        '''
        return get_all_users()
    
    @api.response(201, 'user created successfully')
    @api.doc('create new user')
    @api.expect(_user, validate=True)
    def post(self):
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'User id')
@api.response(404, 'User not found')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        user = get_one_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user