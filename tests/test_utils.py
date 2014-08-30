from flask_application import utils 

import datetime
from tests import BaseTestCase

class TestDatetimeToMillis(BaseTestCase):
    
    def test_should_return_millis_of_datetime(self):
        datetime_value = datetime.datetime(2014, 8, 30, 14, 5, 47, 880026)
        actual_millis = utils.datetime_to_millis(datetime_value)
        expected_millis = 1409378747880 
        self.assertEquals(actual_millis, expected_millis)
