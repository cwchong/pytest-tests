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
