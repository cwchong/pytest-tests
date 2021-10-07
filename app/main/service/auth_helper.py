from app.main.model.user import User
from app.main.service.blacklist_service import save_token


class Auth:
    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    return {
                        'status': 'success',
                        'message': 'Logged in',
                        'Authorization': auth_token
                    }, 200
            else:
                return {
                    'status': 'fail',
                    'message': 'incorrect credentials'
                }, 401
        except Exception as e:
            print(e)
            return {
                'status': 'fail',
                'message': 'try again'
            }, 500
    
    @staticmethod
    def logout_user(data):
        if data:
            print('data is', data)
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            print('resp type is', type(resp))
            if not isinstance(resp, str):
                print('saving token')
                return save_token(token=auth_token)
            else:
                print('NOT saving token')
                return {
                    'status': 'fail',
                    'message': resp
                }, 401
        else:
            return {
                'status': 'fail',
                'message': 'Token is invalid'
            }, 403
    
    @staticmethod
    def get_logged_in_user(new_request):
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                return {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }, 200
            return {
                'status': 'fail',
                'message': resp
            }, 401
        return {
            'status': 'fail',
            'message': 'Please provide valid auth token'
        }, 401
