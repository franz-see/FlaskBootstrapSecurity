from flask.ext.script import Command
from flask_application.populate import populate_data

class ResetDB(Command):
    """Drops all tables and recreates them"""

    def __init__(self, app):
        self.app = app

    def run(self, **kwargs):
        self.app.db.drop_all()
        self.app.db.create_all()

class PopulateDB(Command):
    """Fills in predefined data into DB"""

    def __init__(self, app):
        self.app = app

    def run(self, **kwargs):
        populate_data(self.app)
