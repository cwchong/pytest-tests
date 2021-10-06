import unittest
import pytest

from entrypoint import app, db
from app.main.config import config_by_name


class BaseTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def create_app(self):
        app.config.from_object(config_by_name['test'])
        self.client = app.test_client()
        return app
    
    def setUp(self):
        print('setting up...')
        db.create_all()
        db.session.commit()

    def tearDown(self):
        print('tearing down...')
        db.session.remove()
        db.drop_all()
    