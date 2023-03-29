import pathlib
import unittest

from sdx.datamodel.parsing.topologyhandler import TopologyHandler
from sdx.datamodel.validation.topologyvalidator import TopologyValidator


class TopologyValidatorTests(unittest.TestCase):
    TEST_DATA_DIR = pathlib.Path(__file__).parent.joinpath("data")
    TOPOLOGY_AMLIGHT = TEST_DATA_DIR.joinpath("amlight.json")
    TOPOLOGY_AMPATH = TEST_DATA_DIR.joinpath("ampath.json")
    TOPOLOGY_SAX = TEST_DATA_DIR.joinpath("sax.json")
    TOPOLOGY_ZAOXI = TEST_DATA_DIR.joinpath("zaoxi.json")

    def test_topology_validator_zaoxi(self):
        self._validate_topology(self.TOPOLOGY_ZAOXI)

    def test_topology_validator_ampath(self):
        self._validate_topology(self.TOPOLOGY_AMPATH)

    def test_topology_validator_amlight(self):
        self._validate_topology(self.TOPOLOGY_AMLIGHT)

    def test_topology_validator_sax(self):
        self._validate_topology(self.TOPOLOGY_SAX)

    def _validate_topology(self, path):
        topology = TopologyHandler().import_topology(path)
        validator = TopologyValidator()
        validator.set_topology(topology)
        self.assertTrue(validator.is_valid(), "invalid topology")


if __name__ == "__main__":
    unittest.main()
