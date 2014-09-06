import datetime

from flask_security.utils import encrypt_password
from flask_application.models import User, Todo

def create_roles(app):
    for role in ('admin', 'author'):
        app.user_datastore.create_role(name=role, description=role)
    app.user_datastore.commit()


def create_users(app):
    for u in (('matt@lp.com', 'password', ['admin'], True),
              ('jill@lp.com', 'password', ['author'], True),
              ('tiya@lp.com', 'password', [], False)): 
        app.user_datastore.create_user(email=u[0], password=encrypt_password(u[1]),
                                   roles=u[2], active=u[3], confirmed_at=datetime.datetime.now()
                                  )
        app.user_datastore.commit()

def create_todos(app):
    for u in User.query.all():
        for i in xrange(1, 51):
            todo = Todo(item="Item Todo for %s #%0d" % (u.email, i), date=datetime.datetime.now(), owner=u.id)
            app.db.session.add(todo)
    app.db.session.commit()

def populate_data(app):
    create_roles(app)
    create_users(app)
    create_todos(app)
