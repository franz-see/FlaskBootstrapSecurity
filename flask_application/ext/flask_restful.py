#!/usr/bin/env python

import time

from flask.ext.restful.fields import MarshallingException, Raw

class DateTimeToMillisField(Raw):
    """Return the millis given the datetime"""

    def format(self, value):
        try:
            return int(time.mktime(value.timetuple()) * 1000 + value.microsecond / 1000)
        except AttributeError as ae:
            raise MarshallingException(ae)
