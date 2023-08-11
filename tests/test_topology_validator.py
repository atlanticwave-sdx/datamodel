import unittest

from sdx_datamodel.parsing.topologyhandler import TopologyHandler
from sdx_datamodel.validation.topologyvalidator import TopologyValidator

from . import TestData


class TopologyValidatorTests(unittest.TestCase):
    """
    Tests for TopologyValidator.
    """

    def test_topology_validator_amlight(self):
        validator = self._get_validator(TestData.TOPOLOGY_FILE_AMLIGHT)
        self.assertTrue(validator.is_valid())

    def test_topology_validator_ampath(self):
        validator = self._get_validator(TestData.TOPOLOGY_FILE_AMPATH)

        # AmPath topology JSON fails to validate.
        self.assertFalse(validator.is_valid())

        self.assertRaisesRegex(
            ValueError,
            "Global Institution must be in topology urn:sdx:topology:",
            validator.validate,
        )

        self.assertRaisesRegex(
            ValueError,
            "Location location Address must exist",
            validator.validate,
        )

    def test_topology_validator_sax(self):
        validator = self._get_validator(TestData.TOPOLOGY_FILE_SAX)
        self.assertTrue(validator.is_valid())

    def test_topology_validator_zaoxi(self):
        validator = self._get_validator(TestData.TOPOLOGY_FILE_ZAOXI)
        self.assertTrue(validator.is_valid())

    def _get_validator(self, path):
        topology = TopologyHandler().import_topology(path)
        return TopologyValidator(topology)

    def test_topology_validator_none_location(self):
        """
        Validation must must fail when location values are nil.
        """

        topology = TopologyHandler().import_topology(
            TestData.TOPOLOGY_FILE_AMLIGHT
        )

        topology.nodes[0].location.address = None
        topology.nodes[0].location.latitude = None
        topology.nodes[0].location.longitude = None

        validator = TopologyValidator(topology)
        self.assertFalse(validator.is_valid())

        with self.assertRaises(ValueError) as ex:
            validator.validate()

        errors = ex.exception.args[0].splitlines()

        self.assertEqual(
            errors,
            [
                "Location Longitude must be set to a value",
                "Location Latitude must be set to a value",
                "Location location Address must exist",
                "Location location Address None must be a string",
            ],
        )

    def test_topology_validator_bad_lat_long(self):
        """
        Validation must must fail when location values are nil.
        """

        topology = TopologyHandler().import_topology(
            TestData.TOPOLOGY_FILE_AMLIGHT
        )

        topology.nodes[0].location.address = None
        topology.nodes[0].location.latitude = 200
        topology.nodes[0].location.longitude = 200

        validator = TopologyValidator(topology)
        self.assertFalse(validator.is_valid())

        with self.assertRaises(ValueError) as ex:
            validator.validate()

        errors = ex.exception.args[0].splitlines()
        print(f"errors={errors}")

        self.assertEqual(
            errors,
            [
                "Location Longitude must be a value that is between -180 and 180",
                "Location Latitude must be a value that is between -90 and 90",
                "Location location Address must exist",
                "Location location Address None must be a string",
            ],
        )


if __name__ == "__main__":
    unittest.main()
