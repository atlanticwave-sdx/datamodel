import pathlib
import unittest

from sdx.datamodel.models.location import Location
from sdx.datamodel.parsing.exceptions import DataModelException
from sdx.datamodel.parsing.locationhandler import LocationHandler


class TestPortHandler(unittest.TestCase):
    TEST_DATA_DIR = pathlib.Path(__file__).parent.joinpath("data")
    LOCATION_PATH = TEST_DATA_DIR.joinpath("location.json")

    def testImportLocation(self):
        print("Test Location")
        handler = LocationHandler()
        location = handler.import_location(self.LOCATION_PATH)
        print(f"Location: {location}")

        self.assertIsInstance(location, Location)


if __name__ == "__main__":
    unittest.main()
