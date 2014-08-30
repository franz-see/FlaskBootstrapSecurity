from flask_application import utils 

import datetime
from tests import BaseTestCase

class TestDatetimeToMillis(BaseTestCase):
    
    def test_should_return_millis_of_datetime(self):
        datetime_value = datetime.datetime(2014, 8, 30, 14, 5, 47, 880026)
        actual_millis = utils.datetime_to_millis(datetime_value)
        expected_millis = 1409378747880 
        self.assertEquals(actual_millis, expected_millis)

class _Given_ValueIsNone_When_Get:
    def test_given_value_is_none_then_return_default_value(self):
        actual_value = utils.get({'key':None}, 'key', value_if_none='default value')
        self.assertEquals(actual_value, 'default value')

    def test_key_does_not_exist_then_return_default_value(self):
        actual_value = utils.get({}, 'key', value_if_none='default value')
        self.assertEquals(actual_value, 'default value')

class _Given_MaxValue_WhenGet:
    def test_given_value_is_none(self):
        actual_value = utils.get({'key':None}, 'key', max_value=100)
        self.assertEquals(actual_value, 100)

    def test_given_key_does_not_exist(self):
        actual_value = utils.get({}, 'key', max_value=100)
        self.assertEquals(actual_value, 100)

    def test_given_value_is_above_max_value_then_return_max_value_only(self):
        actual_value = utils.get({'key':101}, 'key', max_value=100)
        self.assertEquals(actual_value, 100)

    def test_given_value_is_below_max_value_then_return_value(self):
        actual_value = utils.get({'key':99}, 'key', max_value=100)
        self.assertEquals(actual_value, 99)

    def test_given_value_is_equal_to_max_value_then_return_value(self):
        actual_value = utils.get({'key':100}, 'key', max_value=100)
        self.assertEquals(actual_value, 100)

class TestGet(BaseTestCase, _Given_ValueIsNone_When_Get, _Given_MaxValue_WhenGet):

    def test_should_get_value_from_dict(self):
        actual_value = utils.get({'dummy key':'dummy value'}, 'dummy key')
        self.assertEquals(actual_value, 'dummy value') 

