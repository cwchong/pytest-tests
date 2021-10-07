import unittest
import json
from app.test.base import BaseTestCase
import pytest


def register_user(self):
    test = self.client.post(
        '/user/',
        data=json.dumps(dict(
            email='test@test.com',
            username='test',
            password='test123'
        )),
        content_type='application/json'
    )
    return test


def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='test@test.com',
            password='test123'
        )),
        content_type='application/json'
    )


def logout_user(self, token):
    return self.client.post(
        '/auth/logout',
        headers=dict(
            Authorization='Bearer {}'.format(token)
        )
    )


class TestAuth(BaseTestCase):
    def test_registration(self):
        user_response = register_user(self)
        response_data = json.loads(user_response.data.decode())
        self.assertTrue(response_data['status'] == 'success')
        self.assertTrue(response_data['message'] == 'successfully registered')
        self.assertTrue(response_data['Authorization'])
        self.assertEqual(user_response.status_code, 201)

    
    def test_registration_with_registered_user(self):
        register_user(self)
        # reg again
        user_response = register_user(self)
        response_data = json.loads(user_response.data.decode())
        self.assertTrue(response_data['status'] == 'fail')
        self.assertTrue(response_data['message'] == 'User already exists, log in')
        self.assertEqual(user_response.status_code, 409)


    def test_registered_user_login(self):
        user_response = register_user(self)
        response_data = json.loads(user_response.data.decode())
        self.assertTrue(response_data['Authorization'])
        self.assertEqual(user_response.status_code, 201)

        # login after registration
        login_response = login_user(self)
        data = json.loads(login_response.data.decode())
        self.assertTrue(data['Authorization'])
        self.assertEqual(login_response.status_code, 200)
    

    def test_valid_logout(self):
        user_response = register_user(self)
        response_data = json.loads(user_response.data.decode())
        self.assertTrue(response_data['Authorization'])
        self.assertEqual(user_response.status_code, 201)

        # login after registration
        login_response = login_user(self)
        data = json.loads(login_response.data.decode())
        self.assertTrue(data['Authorization'])
        self.assertEqual(login_response.status_code, 200)

        # logout test
        logout_response = logout_user(self, data['Authorization'])
        data = json.loads(logout_response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertEqual(logout_response.status_code, 200)

    
    def test_login_unregistered(self):
        login_response = login_user(self)
        data = json.loads(login_response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'incorrect credentials')
        self.assertEqual(login_response.status_code, 401)
    

    def test_logout_blacklisted_token(self):
        user_response = register_user(self)
        response_data = json.loads(user_response.data.decode())
        self.assertTrue(response_data['Authorization'])
        self.assertEqual(user_response.status_code, 201)

        # login after registration
        login_response = login_user(self)
        data = json.loads(login_response.data.decode())
        self.assertTrue(data['Authorization'])
        self.assertEqual(login_response.status_code, 200)

        # logout test; token should be blacklisted now
        logout_response = logout_user(self, data['Authorization'])
        logout_data = json.loads(logout_response.data.decode())
        self.assertTrue(logout_data['status'] == 'success')
        self.assertEqual(logout_response.status_code, 200)

        # logout again with the blacklisted token; status 200 but fail msg
        relogout_response = logout_user(self, data['Authorization'])
        relogout_data = json.loads(relogout_response.data.decode())
        self.assertTrue(relogout_data['status'] == 'fail')
        self.assertTrue(relogout_data['message'] == 'Token logged out, log in again')
        self.assertEqual(relogout_response.status_code, 401)