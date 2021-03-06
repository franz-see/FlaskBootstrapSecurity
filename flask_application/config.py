import logging
import os
import tempfile

class Config(object):
    def __init__(self):
        self.DEBUG = False
        self.TESTING = False
        self.HEROKU = False
        self.PRODUCTION = False

        # import os; os.urandom(24)
        self.SECRET_KEY = '\xe3\xc7\x84:\xcc\x01\xbf\xc1\xee\xec\xc1\x80d\x8c\x1e\x93x;$\xde\x82\t(>'
        self.SITE_NAME = 'Flask Site'
        self.LOG_LEVEL = logging.DEBUG
        self.SERVER_NAME = 'localhost:5000'

        self.SYS_ADMINS = ['foo@example.com']

        # SQLAlchemy support
        self.SQLALCHEMY_DATABASE_URI = os.getenv('FLASK_APPLICATION_SQLALCHEMY_DATABASE_URI')
        self.DB_MAX_PAGE_SIZE = 20
        self.SETUP_DB = False

        # Configured for Gmail
        self.DEFAULT_MAIL_SENDER = os.getenv('FLASK_APPLICATION_DEFAULT_MAIL_SENDER')
        self.MAIL_SERVER = 'smtp.gmail.com'
        self.MAIL_PORT = 465
        self.MAIL_USE_SSL = True
        self.MAIL_USERNAME = os.getenv('FLASK_APPLICATION_MAIL_USERNAME')
        self.MAIL_PASSWORD = os.getenv('FLASK_APPLICATION_MAIL_PASSWORD')

        # Flask-Security setup
        self.SECURITY_EMAIL_SENDER = os.getenv('FLASK_APPLICATION_SECURITY_EMAIL_SENDER')
        self.SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
        self.SECURITY_REGISTERABLE = True
        self.SECURITY_RECOVERABLE = True
        self.SECURITY_URL_PREFIX = '/auth'
        self.SECUIRTY_POST_LOGIN = '/'
        self.SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
        # import uuid; uuid.uuid4().hex
        self.SECURITY_PASSWORD_SALT = '2b8b74efc58e489e879810905b6b6d4dc6'

        self.SECURITY_CONFIRMABLE = True
        self.SECURITY_CHANGEABLE = True

        self.SECURITY_INVALID_LOGIN_MESSAGE = ('Incorrect Username or Password', 'error')

        # CACHE
        self.CACHE_TYPE = 'simple'

        self.CSS_ASSETS_FILTER = None
        self.JS_ASSETS_FILTER = None


class ProductionConfig(Config):
    def __init__(self):
        super(ProductionConfig, self).__init__()
        self.ENVIRONMENT = 'Production'
        self.HEROKU = True
        self.PRODUCTION = True
        self.LOG_LEVEL = logging.INFO
        self.SERVER_NAME = 'example'

        self.MAIL_SERVER = 'smtp.mandrillapp.com'
        self.MAIL_PORT = 465
        self.MAIL_USE_SSL = True
        self.MAIL_USERNAME = os.getenv('FLASK_APPLICATION_MANDRILL_USERNAME')
        self.MAIL_PASSWORD = os.getenv('FLASK_APPLICATION_MANDRILL_APIKEY')

        self.CSS_ASSETS_FILTER = "cssmin"
        self.JS_ASSETS_FILTER = "rjsmin"


class TestConfig(Config):
    def __init__(self):
        super(TestConfig, self).__init__()
        self.ENVIRONMENT = 'Test'
        self.DEBUG = False
        self.TESTING = True
        self.SERVER_NAME = 'localhost:5001'
        self.SQLALCHEMY_DATABASE_URI = "sqlite:///%s/flask_application.db" % tempfile.gettempdir()
        self.LOGIN_DISABLED = False
        self.SETUP_DB = True

class DevelopmentConfig(Config):
    '''
    Use "if app.debug" anywhere in your code,
    that code will run in development mode.
    '''
    def __init__(self):
        super(DevelopmentConfig, self).__init__()
        self.ENVIRONMENT = 'Dev'
        self.DEBUG = True

class DevGunicornConfig(Config):
    def __init__(self):
        super(DevGunicornConfig, self).__init__()
        self.ENVIRONMENT = 'DevGunicorn'
        self.SERVER_NAME = 'localhost:8000'


if os.getenv('TEST') == 'yes':
    app_config = TestConfig()
elif os.getenv('PRODUCTION') == 'yes':
    app_config = ProductionConfig()
elif os.getenv('DEVGUNICORN') == 'yes':
    app_config = DevGunicornConfig()
else:
    app_config = DevelopmentConfig()
