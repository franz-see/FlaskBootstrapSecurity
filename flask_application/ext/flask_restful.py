#!/usr/bin/env python

import copy
from functools import wraps
from sets import Set

from flask.ext.restful import reqparse
from flask.ext.restful.fields import MarshallingException, Raw
from flask_application import utils

class DateTimeToMillisField(Raw):
    """Return the millis given the datetime"""

    def format(self, value):
        try:
            return utils.datetime_to_millis(value)
        except AttributeError as ae:
            raise MarshallingException(ae)


_EXTRA_OPTIONS = Set(['param_name', 'max']) 
class unmarshal_with(object):

    def __init__(self, fields):
        """:param fields: a dict of whose keys will make up the final
                          serialized response output"""
        self.fields = fields

    def __call__(self, f): 
        @wraps(f)
        def wrapper(*args, **kwargs):
            parser = reqparse.RequestParser()
            extra_options = {}
            for arg_name, arg_options in self.fields.iteritems():
                arg_options_copy = copy.deepcopy(arg_options)
                arg_extra_options = {}
                for candidate in arg_options:
                    if candidate in _EXTRA_OPTIONS:
                        arg_extra_options[candidate] = arg_options[candidate]
                        del arg_options_copy[candidate]
                extra_options[arg_name] = arg_extra_options 
                parser.add_argument(arg_name, **arg_options_copy)

            new_kwargs = copy.deepcopy(kwargs) 
            parsed_args = parser.parse_args()
            for arg_name in parsed_args:
                effective_arg_name = extra_options[arg_name]['param_name'] if arg_name in extra_options and 'param_name' in extra_options[arg_name] else arg_name
                arg_value = parsed_args[arg_name] 

                if arg_name in extra_options and 'max' in extra_options[arg_name]:
                    arg_value = min(arg_value, extra_options[arg_name]['max'])

                new_kwargs[effective_arg_name] = arg_value

            return f(*args, **new_kwargs)
        return wrapper
