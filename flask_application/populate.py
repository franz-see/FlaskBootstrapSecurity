import datetime

from flask_security.utils import encrypt_password
from flask_application import app, user_datastore
from flask_application.models import User, Todo

def create_roles():
    for role in ('admin', 'author'):
        user_datastore.create_role(name=role, description=role)
    user_datastore.commit()


def create_users():
    for u in (('matt', 'matt@lp.com', 'password', ['admin'], True),
              ('jill', 'jill@lp.com', 'password', ['author'], True),
              ('tiya', 'tiya@lp.com', 'password', [], False)): 
        user_datastore.create_user(email=u[1], password=encrypt_password(u[2]),
                                   roles=u[3], active=u[4], confirmed_at=datetime.datetime.now()
                                  )
        user_datastore.commit()

def create_todos():
    for u in User.query.all():
        for i in xrange(1, 51):
            todo = Todo(item="Item Todo for %s #%0d" % (u.email, i), date=datetime.datetime.now(), owner=u.id)
            app.db.session.add(todo)
    app.db.session.commit()

def populate_data():
    create_roles()
    create_users()
    create_todos()
