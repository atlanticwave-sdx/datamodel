import unittest

import parsing

from parsing.locationhandler import LocationHandler
from parsing.exceptions import DataModelException

location = './test/data/location.json'

class TestPortHandler(unittest.TestCase):

    def setUp(self):
        self.handler = LocationHandler()  # noqa: E501
    def tearDown(self):
        pass

    def testImportLocation(self):
        try:
            print("Test Location")
            self.handler.import_location(location)
            print(self.handler.location)
        except DataModelException as e:
            print(e)
            return False      
        return True

if __name__ == '__main__':
    unittest.main()