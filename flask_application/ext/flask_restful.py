#!/usr/bin/env python

from flask.ext.restful.fields import MarshallingException, Raw
from flask_application import utils

class DateTimeToMillisField(Raw):
    """Return the millis given the datetime"""

    def format(self, value):
        try:
            return utils.datetime_to_millis(value)
        except AttributeError as ae:
            raise MarshallingException(ae)
