from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns


blueprint = Blueprint('api', __name__)
authorizations = {
    'auth': {
        'type': 'apiKey',
        'in': 'header', 
        'name': 'Authorization'
    }
}

api = Api(blueprint,
        title='flask boilerplate',
        version='1.0',
        description='flask boilerplate only',
        authorizations=authorizations
    )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns, path='/auth')


