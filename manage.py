#!/usr/bin/env python
from flask_application import create_app
from flask_application.config import TestConfig
from flask.ext.script import Manager, Server

from flask_application.script import ResetDB, PopulateDB

from flask.ext.security.script import CreateUserCommand, AddRoleCommand,\
    RemoveRoleCommand, ActivateUserCommand, DeactivateUserCommand

import sys
app = create_app(config=TestConfig()) if sys.argv[1] == 'testserver' else create_app()

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("testserver", Server(host='localhost', port=5001))

manager.add_command("reset_db", ResetDB(app))
manager.add_command("populate_db", PopulateDB(app))

manager.add_command('create_user', CreateUserCommand())
manager.add_command('add_role', AddRoleCommand())
manager.add_command('remove_role', RemoveRoleCommand())
manager.add_command('deactivate_user', DeactivateUserCommand())
manager.add_command('activate_user', ActivateUserCommand())

if __name__ == "__main__":
    manager.run()
