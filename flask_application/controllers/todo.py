#!/usr/bin/env python

from flask import Blueprint 
from flask.ext.restful import Resource, fields, marshal_with
from flask.ext.security import login_required
from flask_login import current_user
from flask_application import app
from flask_application.controllers import TemplateView
from flask_application.ext.flask_restful import DateTimeToMillisField 
from flask_application.models import Todo

todo = Blueprint('todo', __name__, url_prefix='/todo') 

class TodoView(TemplateView):
    blueprint = todo
    route = '/'
    template_name = 'todo/index.html'
    decorators = [login_required]
    
    def get_context_data(self, *args, **kwargs):
        return {}

class TodoListResource(Resource):

    #@marshal_with({'item':fields.String, 'date':DateTimeToMillisField})
    @marshal_with({
        'count':fields.Integer, 
        'results':fields.List(fields.Nested({
            'id':fields.Integer,
            'item':fields.String, 
            'date':DateTimeToMillisField
        })), 
        'pagesize':fields.Integer
    })
    def get(self):
        pagesize = app.config['DB_QUERY_LIMIT']
        count = Todo.query.filter_by(owner=current_user.id).count()
        results = Todo.query.filter_by(owner=current_user.id).limit(pagesize).all()
        return_value = {
            'count' : count,
            'results' : results,
            'pagesize' : pagesize
        }
        print "return value : %s" % return_value
        return return_value
