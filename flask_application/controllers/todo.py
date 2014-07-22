#!/usr/bin/env python

from flask import Blueprint 
from flask.ext.restful import fields, marshal_with, reqparse, Resource
from flask.ext.security import login_required
from flask_login import current_user
from flask_application import app
from flask_application.controllers import TemplateView
from flask_application.ext.flask_restful import DateTimeToMillisField, unmarshal_with 
from flask_application.models import Todo
from flask_application import utils

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
        'results':fields.List(fields.Nested({
            'id':fields.Integer,
            'item':fields.String, 
            'date':DateTimeToMillisField
        })),
        'page':fields.Integer, 
        'page_size':fields.Integer,
        'total_size':fields.Integer 
    })
    @unmarshal_with({
        's' : { 'param_name' : 'page_size', 'type' : int, 'default' : app.config['DB_MAX_PAGE_SIZE'], 'max' : app.config['DB_MAX_PAGE_SIZE'] },
        'p' : { 'param_name' : 'page', 'type' : int, 'default' : 1 }
    })
    def get(self, page_size, page):
        total_size = Todo.query.filter_by(owner=current_user.id).count()
        results = Todo.query.filter_by(owner=current_user.id).offset((page-1) * page_size).limit(page_size).all()
        return {
            'results' : results,
            'page' : page,
            'page_size' : page_size,
            'total_size' : total_size
        }
