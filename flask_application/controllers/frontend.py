#!/usr/bin/env python

import datetime

from flask import current_app, Blueprint
from flask.ext.security import login_required

from flask_application.controllers import TemplateView

frontend = Blueprint('frontend', __name__)


class IndexView(TemplateView):
    blueprint = frontend
    route = '/'
    template_name = 'home/index.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'now': datetime.datetime.now(),
            'config': current_app.config
        }


class ProfileView(TemplateView):
    blueprint = frontend
    route = '/profile'
    template_name = 'profiles/profile.html'
    decorators = [login_required]

    def get_context_data(self, *args, **kwargs):
        return {
            'content': 'This is the profile page'
        }
