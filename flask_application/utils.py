#!/usr/bin/env python

import time

def datetime_to_millis(value): 
    return int(time.mktime(value.timetuple()) * 1000 + value.microsecond / 1000)

def get(d, key, value_if_none=None, max_value=None):
    effective_value_if_none = value_if_none or max_value
    effective_value = d.get(key, effective_value_if_none) or effective_value_if_none
    return min(effective_value, max_value) if max_value else effective_value

