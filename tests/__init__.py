from flask.ext.testing import TestCase
from flask_application import create_app
from flask_application.config import TestConfig

class BaseTestCase(TestCase):

    def create_app(self):
        self.app = create_app(config=TestConfig())
        return self.app

    def setUp(self):
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.drop_all()
