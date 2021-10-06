import os
import unittest
import pytest

from flask import current_app
from app.main.config import basedir
from app.main import create_app


# some basic testing
class TestDevelopmentConfig(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def initclient(self):
        self.app = create_app('dev')
    
    def test_app_is_development(self, ):
        app = self.app
        self.assertFalse(app.config['SECRET_KEY'] is 'my_wrong_key')
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
        )


class TestTestingConfig(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def initclient(self):
        self.app = create_app('test')
    
    def test_app_is_testing(self):
        app = self.app
        self.assertFalse(app.config['SECRET_KEY'] is 'my_wrong_key')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(current_app is None)
        print(app.config['SQLALCHEMY_DATABASE_URI'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
        )


class TestProductionConfig(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def initclient(self):
        self.app = create_app('prod')
    
    def test_app_is_production(self):
        app = self.app
        self.assertFalse(app.config['SECRET_KEY'] is 'my_wrong_key')
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        self.assertFalse(current_app is None)
        
         