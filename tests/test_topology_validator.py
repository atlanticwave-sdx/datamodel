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


if __name__ == "__main__":
    unittest.main()
