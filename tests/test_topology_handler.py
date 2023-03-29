import pathlib
import unittest

from sdx.datamodel.models.topology import Topology
from sdx.datamodel.parsing.exceptions import MissingAttributeException
from sdx.datamodel.parsing.topologyhandler import TopologyHandler


class TopologyHandlerTests(unittest.TestCase):
    TEST_DATA_DIR = pathlib.Path(__file__).parent.joinpath("data")
    TOPOLOGY_AMLIGHT = TEST_DATA_DIR.joinpath("amlight.json")

    def test_import_topology(self):
        topology = TopologyHandler().import_topology(self.TOPOLOGY_AMLIGHT)
        print(f"Topology: {topology}")
        self.assertIsInstance(topology, Topology)

    def test_import_topology_nodes(self):
        print("Test Nodes: at least one:")
        topology = TopologyHandler().import_topology(self.TOPOLOGY_AMLIGHT)

        print(f"Nodes[0]: {topology.nodes[0]}")
        self.assertTrue(topology.nodes is not None)
        self.assertTrue(len(topology.nodes) != 0)

    def test_import_topology_links(self):
        print("Test Links: at least one")
        topology = TopologyHandler().import_topology(self.TOPOLOGY_AMLIGHT)

        print(f"Links: {topology.links[0]}")
        self.assertTrue(topology.links is not None)
        self.assertTrue(len(topology.links) != 0)


if __name__ == "__main__":
    unittest.main()
