#!/usr/bin/env python

import datetime

from flask import Blueprint 
from flask.ext.restful import Resource, fields, marshal_with
from flask.ext.security import login_required
from flask_application.controllers import TemplateView
from flask_application.ext.flask_restful import DateTimeToMillisField 
from flask_application.models import Todo
from flask_login import current_user

todo = Blueprint('todo', __name__, url_prefix='/todo') 

class TodoView(TemplateView):
    blueprint = todo
    route = '/'
    template_name = 'todo/index.html'
    decorators = [login_required]
    
    def get_context_data(self, *args, **kwargs):
        return {}

class TodoListResource(Resource):

    @marshal_with({'item':fields.String, 'date':DateTimeToMillisField})
    def get(self):
        results = [{'item': "Moroni", 'date':datetime.datetime(2014,07,01) },
                {'item': "Tiancum", 'date':datetime.datetime(2013,01,02) },
                {'item': "Jacob", 'date':datetime.datetime(2014,03,05) },
                {'item': "Nephi", 'date':datetime.datetime(2015,11,07) },
                {'item': "Enos", 'date':datetime.datetime(2014,10,13) }
               ]
        results = Todo.query.filter_by(owner=current_user.id).all()
        return results
