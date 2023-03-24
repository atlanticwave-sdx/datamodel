import unittest

from sdx.datamodel.parsing.exceptions import DataModelException
from sdx.datamodel.parsing.locationhandler import LocationHandler

location = "./tests/data/location.json"


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


if __name__ == "__main__":
    unittest.main()
