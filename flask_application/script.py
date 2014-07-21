from flask.ext.script import Command
from flask_application.populate import populate_data
from flask_application import app

class ResetDB(Command):
    """Drops all tables and recreates them"""
    def run(self, **kwargs):
        app.db.drop_all()
        app.db.create_all()

class PopulateDB(Command):
    """Fills in predefined data into DB"""
    def run(self, **kwargs):
        populate_data()
