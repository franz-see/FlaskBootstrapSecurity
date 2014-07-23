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

    def __init__(self, fields, in_object=None):
        """:param fields: a dict of whose keys will make up the final
                          serialized response output"""
        self.fields = fields
        self.in_object = in_object

    def _separate_options_from_extra_options(self):
        options = {}
        extra_options = {}
        for arg_name, all_options in self.fields.iteritems():
            arg_options = {}
            arg_extra_options = {}
            for option in all_options:
                if option in _EXTRA_OPTIONS:
                    arg_extra_options[option] = all_options[option]
                else:
                    arg_options[option] = all_options[option]
            extra_options[arg_name] = arg_extra_options
            options[arg_name] = arg_options
        return options, extra_options

    @staticmethod
    def _create_parser(parser_options):
        parser = reqparse.RequestParser()
        for arg_name, parser_option in parser_options.iteritems():
            parser.add_argument(arg_name, **parser_option)
        return parser

    @staticmethod
    def _extract_parameters(parser, extra_options, kwargs):
        new_kwargs = copy.deepcopy(kwargs)
        parsed_args = parser.parse_args()
        for arg_name in parsed_args:
            effective_arg_name = extra_options[arg_name]['param_name'] if arg_name in extra_options and 'param_name' in extra_options[arg_name] else arg_name
            arg_value = parsed_args[arg_name]

            if arg_name in extra_options and 'max' in extra_options[arg_name]:
                arg_value = min(arg_value, extra_options[arg_name]['max'])

            new_kwargs[effective_arg_name] = arg_value
        return new_kwargs

    def _assemble_args(self, args, parameters):
        new_args = args
        new_kwargs = {}
        if self.in_object:
            new_args = args + (self.in_object(**parameters),)
        else:
            new_kwargs = parameters
        return new_args, new_kwargs

    def __call__(self, f): 
        @wraps(f)
        def wrapper(*args, **kwargs):
            options, extra_options = self._separate_options_from_extra_options()
            parser = self._create_parser(options)
            parameters = self._extract_parameters(parser, extra_options, kwargs)
            new_args, new_kwargs = self._assemble_args(args, parameters)
            return f(*new_args, **new_kwargs)
        return wrapper
