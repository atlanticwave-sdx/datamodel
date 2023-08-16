import unittest

from sdx_datamodel.models.topology import Topology
from sdx_datamodel.parsing.topologyhandler import TopologyHandler

from . import TestData


class TopologyHandlerTests(unittest.TestCase):
    def test_import_topology(self):
        topology = TopologyHandler().import_topology(
            TestData.TOPOLOGY_FILE_AMLIGHT
        )
        print(f"Topology: {topology}")
        self.assertIsInstance(topology, Topology)

    def test_topology_setters(self):
        topology = TopologyHandler().import_topology(
            TestData.TOPOLOGY_FILE_AMLIGHT
        )
        self.assertIsInstance(topology, Topology)

        with self.assertRaises(ValueError) as ex:
            topology.set_name(None)

        self.assertIn(
            "Invalid value for `name`, must not be `None`", ex.exception.args
        )

        with self.assertRaises(ValueError) as ex:
            topology.set_id(None)

        self.assertIn(
            "Invalid value for `id`, must not be `None`", ex.exception.args
        )

    def test_import_topology_nodes(self):
        print("Test Nodes: at least one:")
        topology = TopologyHandler().import_topology(
            TestData.TOPOLOGY_FILE_AMLIGHT
        )

        print(f"Nodes[0]: {topology.nodes[0]}")
        self.assertTrue(topology.nodes is not None)
        self.assertTrue(len(topology.nodes) != 0)

    def test_import_topology_links(self):
        print("Test Links: at least one")
        topology = TopologyHandler().import_topology(
            TestData.TOPOLOGY_FILE_AMLIGHT
        )

        print(f"Links: {topology.links[0]}")
        self.assertTrue(topology.links is not None)
        self.assertTrue(len(topology.links) != 0)


if __name__ == "__main__":
    unittest.main()
