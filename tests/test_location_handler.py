import pathlib
import unittest

from sdx.datamodel.models.location import Location
from sdx.datamodel.parsing.exceptions import DataModelException
from sdx.datamodel.parsing.locationhandler import LocationHandler


class LocationHandlerTests(unittest.TestCase):
    TEST_DATA_DIR = pathlib.Path(__file__).parent.joinpath("data")
    LOCATION_PATH = TEST_DATA_DIR.joinpath("location.json")

    def test_import_location(self):
        location = LocationHandler().import_location(self.LOCATION_PATH)
        print(f"Location: {location}")

        self.assertIsInstance(location, Location)
        self.assertEqual(location.address, "Miami")
        self.assertEqual(location.latitude, -28.51107891831147)
        self.assertEqual(location.longitude, -79.57947854792273)

    def test_import_empty_location(self):
        location = LocationHandler().import_location_data({})
        print(f"Location: {location}")

        self.assertIsInstance(location, Location)
        self.assertIsNone(location.address)
        self.assertIsNone(location.latitude)
        self.assertIsNone(location.longitude)

    def test_import_null_location(self):
        self.assertRaisesRegex(
            TypeError,
            "expected str, bytes or os.PathLike object, not NoneType",
            LocationHandler().import_location,
            None,
        )


if __name__ == "__main__":
    unittest.main()
