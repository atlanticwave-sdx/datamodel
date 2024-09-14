import json
import unittest

from sdx_datamodel.models.connection import Connection
from sdx_datamodel.parsing.connectionhandler import ConnectionHandler
from sdx_datamodel.parsing.exceptions import MissingAttributeException

from . import TestData


class ConnectionHandlerTests(unittest.TestCase):
    """Test ConnectionHandler class."""

    def test_import_connection_p2p(self):
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_P2P
        )
        self.assertIsInstance(connection, Connection)

    def test_import_connection_req(self):
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_REQ
        )
        self.assertIsInstance(connection, Connection)

    def test_import_connection_req_no_node(self):
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_REQ_NO_NODE
        )
        self.assertIsInstance(connection, Connection)

    def test_connection_setters(self):
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_P2P
        )

        self.assertIsInstance(connection, Connection)

        with self.assertRaises(ValueError) as ex:
            connection.name = None

        self.assertIn(
            "Invalid value for `name`, must not be `None`", ex.exception.args
        )

        with self.assertRaises(ValueError) as ex:
            connection.id = None

        self.assertIn(
            "Invalid value for `id`, must not be `None`", ex.exception.args
        )

    def test_import_connection_missing_required_attributes(self):
        """Exception expected when required attributes are missing."""
        data = {}
        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing required attribute 'id' while parsing <{data}>",
            ConnectionHandler().import_connection_data,
            data,
        )

        data = {"id": "id"}
        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing required attribute 'name' while parsing <{data}>",
            ConnectionHandler().import_connection_data,
            data,
        )

        data = {"id": "id", "name": "name"}
        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing required attribute 'ingress_port' while parsing <{data}>",
            ConnectionHandler().import_connection_data,
            data,
        )

        data = {"id": "id", "name": "name", "endpoints": None}
        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing required attribute 'ingress_port' while parsing <{data}>",
            ConnectionHandler().import_connection_data,
            data,
        )

        data = {
            "id": "id",
            "name": "name",
            "ingress_port": {"id": "urn:ingress", "name": "test"},
            "egress_port": None,
        }
        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing required attribute 'egress_port' while parsing <{data}>",
            ConnectionHandler().import_connection_data,
            data,
        )

        data = {"id": "id", "egress_port": None, "ingress_port": None}
        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing required attribute 'name' while parsing <{data}>",
            ConnectionHandler().import_connection_data,
            data,
        )

    def test_import_connection_missing_optional_attributes(self):
        # All required attributes are set, so no error expected when
        # optional attributes are missing.
        ingress_port = {"id": "ingress_port_id", "name": "ingress_port_name"}
        egress_port = {"id": "egress_port_id", "name": "egress_port_name"}
        connection = ConnectionHandler().import_connection_data(
            {
                "id": "id",
                "name": "name",
                "ingress_port": ingress_port,
                "egress_port": egress_port,
            }
        )

        self.assertIsInstance(connection, Connection)

        self.assertIsInstance(connection.swagger_types, dict)
        self.assertIsInstance(connection.attribute_map, dict)

        self.assertEqual(connection.id, "id")
        self.assertEqual(connection.name, "name")

        self.assertIsNotNone(connection.egress_port)
        self.assertIsNotNone(connection.ingress_port)

        self.assertIsNone(connection.status)
        self.assertIsNone(connection.start_time)
        self.assertIsNone(connection.end_time)

        self.assertIsInstance(connection.to_dict(), dict)
        self.assertIsInstance(connection.to_str(), str)

        self.assertEqual(connection.latency_required, None)
        connection.latency_required = 10
        self.assertEqual(connection.latency_required, 10)

        self.assertEqual(connection.bandwidth_required, None)
        connection.bandwidth_required = 10
        self.assertEqual(connection.bandwidth_required, 10)

        self.assertRaisesRegex(
            ValueError,
            "Invalid value for `ingress_port`: must not be `None`",
            connection.set_ingress_port,
            None,
        )

        self.assertRaisesRegex(
            TypeError,
            "Invalid type for `ingress_port`: must be of type `Port`",
            connection.set_ingress_port,
            {},
        )

        self.assertRaisesRegex(
            ValueError,
            "Invalid value for `egress_port`: must not be `None`",
            connection.set_egress_port,
            None,
        )

        self.assertRaisesRegex(
            TypeError,
            "Invalid type for `egress_port`, must be of type `Port`",
            connection.set_egress_port,
            {},
        )

    def test_connection_handler_no_ingress_port(self):
        connection_data = json.loads(TestData.CONNECTION_FILE_P2P.read_text())
        connection_data["ingress_port"] = None

        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing required attribute 'ingress_port' while parsing <{connection_data}>",
            ConnectionHandler().import_connection_data,
            connection_data,
        )

    def test_connection_handler_no_egress_port(self):
        connection_data = json.loads(TestData.CONNECTION_FILE_P2P.read_text())
        connection_data["egress_port"] = None

        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing required attribute 'egress_port' while parsing <{connection_data}>",
            ConnectionHandler().import_connection_data,
            connection_data,
        )

    """Test ConnectionHandler class for Port P2P Connection Request Spec v2."""

    def test_import_connection_port_p2p_v2(self):
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_L2VPN_P2P_V1
        )
        self.assertIsInstance(connection, Connection)

        data = {
            "name": "new-connection",
            "endpoints": [
                {"port_id": "id1", "vlan": "777"},
                {"port_id": "id2"},
            ],
        }
        with self.assertRaises(MissingAttributeException):
            connection = ConnectionHandler().import_connection_data(data)


if __name__ == "__main__":
    unittest.main()
