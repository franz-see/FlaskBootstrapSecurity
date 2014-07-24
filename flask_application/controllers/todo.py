#!/usr/bin/env python

from datetime import datetime

from flask import Blueprint
from flask.ext.restful import fields, marshal_with, Resource
from flask.ext.security import login_required
from flask_login import current_user
from sqlalchemy import and_

from flask_application import app
from flask_application.controllers import TemplateView
from flask_application.ext.flask_restful import DateTimeToFormattedString, unmarshal_with
from flask_application.models import Todo

todo_blueprint = Blueprint('todo', __name__, url_prefix='/todo')

DATE_FORMAT = '%B %d, %Y'

class TodoView(TemplateView):
    blueprint = todo_blueprint
    route = '/'
    template_name = 'todo/index.html'
    decorators = [login_required]
    
    def get_context_data(self, *args, **kwargs):
        return {}

class TodoResource(Resource):

    @unmarshal_with({
        's' : { 'param_name' : 'page_size', 'type' : int, 'default' : app.config['DB_MAX_PAGE_SIZE'], 'max' : app.config['DB_MAX_PAGE_SIZE'] },
        'p' : { 'param_name' : 'page', 'type' : int, 'default' : 1 }
    })
    @marshal_with({
        'results':fields.List(fields.Nested({
            'id':fields.Integer,
            'item':fields.String, 
            'date':DateTimeToFormattedString(DATE_FORMAT)
        })),
        'page':fields.Integer, 
        'page_size':fields.Integer,
        'total_size':fields.Integer 
    })
    def get(self, page_size, page):
        total_size = Todo.query.filter_by(owner=current_user.id).count()
        results = Todo.query.filter_by(owner=current_user.id).order_by(Todo.date.desc(), Todo.id.desc()).offset((page-1) * page_size).limit(page_size).all()
        return {
            'results' : results,
            'page' : page,
            'page_size' : page_size,
            'total_size' : total_size
        }

    @unmarshal_with({
        'id' : { 'type' : int },
        'item' : {},
        'date' : { 'type' : (lambda v,n:datetime.strptime(v, DATE_FORMAT)) }
    }, in_object=Todo)
    @marshal_with({
        'id' : fields.Integer,
        'item':fields.String,
        'date':DateTimeToFormattedString(DATE_FORMAT)
    })
    def post(self, todo_arg):
        if todo_arg.id:
            todo_model = self._find_todo(todo_arg.id)
            todo_model.date = todo_arg.date
            todo_model.item = todo_arg.item
        else:
            todo_model = todo_arg
            todo_model.owner = current_user.id
            app.db.session.add(todo_model)

        app.db.session.commit()
        return todo_model

    def delete(self, todo_id):
        todoToBeDeleted = self._find_todo(todo_id)
        if not todoToBeDeleted:
            return "fail"
        app.db.session.delete(todoToBeDeleted)
        app.db.session.commit()
        return "success"

    @staticmethod
    def _find_todo(id):
        return Todo.query.filter(and_(Todo.id==id, Todo.owner==current_user.id)).first()
