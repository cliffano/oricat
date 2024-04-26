# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import os
import unittest
from oricat import categorise

class TestConstructor(unittest.TestCase):

    def test_constructor_with_aws_region_with_invalid_keys(self):
        os.environ['AWS_DEFAULT_REGION'] = 'ap-southeast-2'
        os.environ['AWS_ACCESS_KEY_ID'] = 'someaccesskeyid'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'somesecretaccesskey'
        categorise('in', 'out')
