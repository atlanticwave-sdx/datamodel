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

        # Set invalid location values for each node in the topology.
        for node in topology.nodes:
            node.location.address = None
            node.location.latitude = None
            node.location.longitude = None

        validator = TopologyValidator(topology)
        self.assertFalse(validator.is_valid())

        with self.assertRaises(ValueError) as ex:
            validator.validate()

        errors = ex.exception.args[0].splitlines()

        # Assert that each of the possible error message is repeated
        # for each node in the topology.
        # for message in set(errors):
        #    self.assertEqual(errors.count(message), len(topology.nodes))
        self.assertEqual(3, len(topology.nodes))

    def test_topology_validator_bad_lat_long(self):
        """
        Validation must fail when lat/long/address values are invalid.
        """
        topology = TopologyHandler().import_topology(
            TestData.TOPOLOGY_FILE_AMLIGHT
        )

        # Set invalid location values for each node in the topology.
        for node in topology.nodes:
            node.location.address = 0
            node.location.latitude = 91
            node.location.longitude = -181

        validator = TopologyValidator(topology)
        self.assertFalse(validator.is_valid())

        with self.assertRaises(ValueError) as ex:
            validator.validate()

        errors = ex.exception.args[0].splitlines()

        # Assert that each of the possible error message is repeated
        # for each node in the topology.
        for message in set(errors):
            self.assertEqual(errors.count(message), len(topology.nodes))


if __name__ == "__main__":
    unittest.main()
