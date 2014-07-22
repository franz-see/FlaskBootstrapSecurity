#!/usr/bin/env python

from flask import Blueprint 
from flask.ext.restful import fields, marshal_with, reqparse, Resource
from flask.ext.security import login_required
from flask_login import current_user
from flask_application import app
from flask_application.controllers import TemplateView
from flask_application.ext.flask_restful import DateTimeToMillisField 
from flask_application.models import Todo

todo = Blueprint('todo', __name__, url_prefix='/todo') 


parser = reqparse.RequestParser()
parser.add_argument('p', type=int)
parser.add_argument('s', type=int)

class TodoView(TemplateView):
    blueprint = todo
    route = '/'
    template_name = 'todo/index.html'
    decorators = [login_required]
    
    def get_context_data(self, *args, **kwargs):
        return {}

class TodoListResource(Resource):

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
        args = parser.parse_args()

        db_max_page_size = app.config['DB_MAX_PAGE_SIZE']
        page_size = args['s'] if ('s' in args and args['s'] and args['s'] <= db_max_page_size) else db_max_page_size
        page = args['p'] or 1

        count = Todo.query.filter_by(owner=current_user.id).count()
        results = Todo.query.filter_by(owner=current_user.id).offset((page-1) * page_size).limit(page_size).all()
        return {
            'count' : count,
            'results' : results,
            'pagesize' : page_size
        }
