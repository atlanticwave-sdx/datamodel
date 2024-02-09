import unittest

from sdx_datamodel.models.location import Location
from sdx_datamodel.parsing.locationhandler import LocationHandler

from . import TestData


class LocationHandlerTests(unittest.TestCase):
    def test_import_location(self):
        location = LocationHandler().import_location(TestData.LOCATION_FILE)
        print(f"Location: {location}")

        self.assertIsInstance(location, Location)
        self.assertEqual(location.address, "Miami")
        self.assertEqual(location.latitude, -28.51107891831147)
        self.assertEqual(location.longitude, -79.57947854792273)
        self.assertEqual(location.iso3166_2_lvl4, "US-MIA")

    def test_import_empty_location(self):
        location = LocationHandler().import_location_data({})
        print(f"Location: {location}")

        self.assertIsInstance(location, Location)
        self.assertIsNone(location.address)
        self.assertIsNone(location.latitude)
        self.assertIsNone(location.longitude)
        self.assertIsNone(location.iso3166_2_lvl4)

    def test_import_null_location(self):
        self.assertRaisesRegex(
            TypeError,
            "expected str, bytes or os.PathLike object, not NoneType",
            LocationHandler().import_location,
            None,
        )

    def test_compare_location(self):
        location1 = LocationHandler().import_location(TestData.LOCATION_FILE)
        location2 = LocationHandler().import_location(TestData.LOCATION_FILE)
        self.assertEqual(location1, location2)


if __name__ == "__main__":
    unittest.main()
