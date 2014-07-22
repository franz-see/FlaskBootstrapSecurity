#!/usr/bin/env python

import time

def datetime_to_millis(value): 
    return int(time.mktime(value.timetuple()) * 1000 + value.microsecond / 1000)

