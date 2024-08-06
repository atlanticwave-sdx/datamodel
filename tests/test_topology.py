import json
import unittest
from unittest.mock import MagicMock, patch

from sdx_datamodel.models.link import Link
from sdx_datamodel.models.service import Service
from sdx_datamodel.models.topology import Topology
from sdx_datamodel.parsing.servicehandler import ServiceHandler
from sdx_datamodel.parsing.topologyhandler import TopologyHandler

from . import TestData


class TopologyTests(unittest.TestCase):
    def test_get_node_by_port(self):
        topology = TopologyHandler().import_topology(
            TestData.TOPOLOGY_FILE_AMLIGHT
        )
        node = topology.get_node_by_port("urn:sdx:port:amlight.net:B1:2")
        self.assertIsNotNone(node)
        self.assertEqual(node.name, "amlight:Novi01")
        self.assertEqual(node.id, "urn:sdx:node:amlight.net:B1")

    def test_get_port_by_link(self):
        topology = TopologyHandler().import_topology(
            TestData.TOPOLOGY_FILE_AMLIGHT
        )
        n1, port1, n2, port2 = topology.get_port_by_link(
            "urn:sdx:node:amlight.net:B1", "urn:sdx:node:amlight.net:B2"
        )
        self.assertIsNotNone(port1)
        self.assertIsNotNone(port2)

        n1, port1, n2, port2 = topology.get_port_by_link(
            "urn:sdx:node:amlight.net:B2", "urn:sdx:node:amlight.net:B1"
        )
        self.assertIsNotNone(port1)
        self.assertIsNotNone(port2)

    def test_has_node_by_id(self):
        topology = TopologyHandler().import_topology(
            TestData.TOPOLOGY_FILE_AMLIGHT
        )
        self.assertTrue(topology.has_node_by_id("urn:sdx:node:amlight.net:B1"))
        self.assertFalse(topology.has_node_by_id("node3"))

    def test_remove_node(self):
        topology = TopologyHandler().import_topology(
            TestData.TOPOLOGY_FILE_AMLIGHT
        )
        node_id = "urn:sdx:node:amlight.net:B1"
        self.assertTrue(topology.has_node_by_id(node_id))

        topology.remove_node(node_id)

        self.assertFalse(topology.has_node_by_id(node_id))

    def test_set_service(self):
        topology = TopologyHandler().import_topology(
            TestData.TOPOLOGY_FILE_AMLIGHT
        )
        service = ServiceHandler().import_service(TestData.SERVICE_FILE)
        topology.set_service(service.to_dict())
        self.assertEqual(topology.services.owner, "FIU")

    def test_set_ports(self):
        topology = TopologyHandler().import_topology(
            TestData.TOPOLOGY_FILE_AMLIGHT
        )
        n1, port1, n2, port2 = topology.get_port_by_link(
            "urn:sdx:node:amlight.net:B1", "urn:sdx:node:amlight.net:B2"
        )
        ports = [port1, port2]
        link = Link()
        link.set_ports([port1, port2])
        self.assertEqual(link.ports, ports)

    def test_setter_nodes(self):
        """Test Topology.nodes setter."""
        topo = Topology(nodes=[], links=[])
        topo._update_port_by_id = MagicMock()
        with self.assertRaises(ValueError):
            topo.nodes = None
        topo.nodes = []
        topo._update_port_by_id.assert_called_with([])

        topo.add_nodes([1])
        topo._update_port_by_id.assert_called_with([1])
