from flask.ext.testing import TestCase
from flask_application import create_app
from flask_application.config import TestConfig

class BaseTestCase(TestCase):

    def create_app(self):
        return create_app(config=TestConfig())
