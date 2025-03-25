import json
import unittest
from pathlib import Path

from pydantic import ValidationError

from sdx_datamodel.models.connection_request import (
    ConnectionRequest,
    ConnectionRequestV0,
    ConnectionRequestV1,
)

from . import TestData


def make_connection_request_from_json(path: Path) -> ConnectionRequest:
    # data = json.loads(path.read_text())
    data = path.read_text()
    return ConnectionRequest.model_validate_json(data)


class ConnectionHandlerTests(unittest.TestCase):
    """Test ConnectionHandler class."""

    def test_import_connection_p2p(self):
        c = make_connection_request_from_json(TestData.CONNECTION_FILE_P2P_v0)
        self.assertIsInstance(c, ConnectionRequest)
        self.assertIsInstance(c.root, ConnectionRequestV0)

    def test_import_connection_req(self):
        c = make_connection_request_from_json(TestData.CONNECTION_FILE_REQ_v0)
        self.assertIsInstance(c, ConnectionRequest)
        self.assertIsInstance(c.root, ConnectionRequestV0)

    def test_import_connection_req_no_node(self):
        c = make_connection_request_from_json(
            TestData.CONNECTION_FILE_REQ_NO_NODE_v0
        )
        self.assertIsInstance(c, ConnectionRequest)
        self.assertIsInstance(c.root, ConnectionRequestV0)

    def test_connection_setters(self):
        c = make_connection_request_from_json(TestData.CONNECTION_FILE_P2P_v0)
        self.assertIsInstance(c, ConnectionRequest)
        self.assertIsInstance(c.root, ConnectionRequestV0)

        # `name` property exists, but we can't assign to it.
        self.assertIsNotNone(c.name)

        with self.assertRaises(ValueError) as ex:
            c.name = None

        self.assertIn(
            '"ConnectionRequest" object has no field "name"', ex.exception.args
        )

        # `id` property exists, but we can't assign to it.
        self.assertIsNotNone(c.id)

        with self.assertRaises(ValueError) as ex:
            c.id = None

        self.assertIn(
            '"ConnectionRequest" object has no field "id"', ex.exception.args
        )

    def test_import_connection_missing_required_attributes(self):
        """Exception expected when required attributes are missing."""

        # All three required fields (id, ingress_port, and
        # egress_port) are missing in input data.
        self.assertRaisesRegex(
            ValidationError,
            "3 validation errors for ConnectionRequest",
            ConnectionRequestV0.model_validate,
            {},
        )

        # data = {"id": "id"}
        # self.assertRaisesRegex(
        #     MissingAttributeException,
        #     f"Missing required attribute 'name' while parsing <{data}>",
        #     ConnectionHandler().import_connection_data,
        #     data,
        # )

        # missing ingress_port and egress_port.
        self.assertRaisesRegex(
            ValidationError,
            "2 validation errors for ConnectionRequest",
            ConnectionRequestV0.model_validate,
            {"id": "id"},
        )

        # data = {"id": "id", "name": "name"}
        # self.assertRaisesRegex(
        #     MissingAttributeException,
        #     f"Missing required attribute 'ingress_port' while parsing <{data}>",
        #     ConnectionHandler().import_connection_data,
        #     data,
        # )

        # missing ingress_port and egress_port.
        self.assertRaisesRegex(
            ValidationError,
            "2 validation errors for ConnectionRequest",
            ConnectionRequestV0.model_validate,
            {"id": "id", "name": "name"},
        )

        # missing ingress_port and egress_port.
        self.assertRaisesRegex(
            ValidationError,
            "2 validation errors for ConnectionRequestV0",
            ConnectionRequestV0.model_validate,
            {"id": "id", "name": "name", "endpoints": None},
        )

        # `endpoints` should be a valid list
        self.assertRaisesRegex(
            ValidationError,
            "1 validation error for ConnectionRequest",
            ConnectionRequestV1.model_validate,
            {"id": "id", "name": "name", "endpoints": None},
        )

        # data = {
        #     "id": "id",
        #     "name": "name",
        #     "ingress_port": {"id": "urn:ingress", "name": "test"},
        #     "egress_port": None,
        # }
        # self.assertRaisesRegex(
        #     MissingAttributeException,
        #     f"Missing required attribute 'egress_port' while parsing <{data}>",
        #     ConnectionHandler().import_connection_data,
        #     data,
        # )

        # invalid `egress_port`.
        self.assertRaisesRegex(
            ValidationError,
            "1 validation error for ConnectionRequestV0",
            ConnectionRequestV0.model_validate,
            {
                "id": "id",
                "name": "name",
                "ingress_port": {"id": "urn:ingress", "name": "test"},
                "egress_port": None,
            },
        )

        # data = {"id": "id", "egress_port": None, "ingress_port": None}
        # self.assertRaisesRegex(
        #     MissingAttributeException,
        #     f"Missing required attribute 'name' while parsing <{data}>",
        #     ConnectionHandler().import_connection_data,
        #     data,
        # )

        # Both `egress_port` and `ingress_port` are invalid.
        self.assertRaisesRegex(
            ValidationError,
            "2 validation errors for ConnectionRequestV0",
            ConnectionRequestV0.model_validate,
            {"id": "id", "egress_port": None, "ingress_port": None},
        )

    def test_import_connection_missing_optional_attributes(self):
        # All required attributes are set, so no error expected when
        # optional attributes are missing.
        # ingress_port = {"id": "ingress_port_id", "name": "ingress_port_name"}
        # egress_port = {"id": "egress_port_id", "name": "egress_port_name"}
        # connection = ConnectionHandler().import_connection_data(
        #     {
        #         "id": "id",
        #         "name": "name",
        #         "ingress_port": ingress_port,
        #         "egress_port": egress_port,
        #     }
        # )

        connection = ConnectionRequestV0.model_validate(
            {
                "id": "id",
                "name": "name",
                "ingress_port": {
                    "id": "ingress_port_id",
                    "name": "ingress_port_name",
                },
                "egress_port": {
                    "id": "egress_port_id",
                    "name": "egress_port_name",
                },
            }
        )

        self.assertIsInstance(connection, ConnectionRequestV0)

        # self.assertIsInstance(connection.swagger_types, dict)
        # self.assertIsInstance(connection.attribute_map, dict)

        self.assertEqual(connection.id, "id")
        self.assertEqual(connection.name, "name")

        self.assertIsNotNone(connection.egress_port)
        self.assertIsNotNone(connection.ingress_port)

        # self.assertIsNone(connection.status)
        # self.assertIsNone(connection.start_time)
        # self.assertIsNone(connection.end_time)

        # self.assertIsInstance(connection.to_dict(), dict)
        # self.assertIsInstance(connection.to_str(), str)

        self.assertEqual(connection.latency_required, 0)
        # connection.latency_required = 10
        # self.assertEqual(connection.latency_required, 10)

        self.assertEqual(connection.bandwidth_required, 0)
        # connection.bandwidth_required = 10
        # self.assertEqual(connection.bandwidth_required, 10)

        # self.assertRaisesRegex(
        #     ValueError,
        #     "Invalid value for `ingress_port`: must not be `None`",
        #     connection.set_ingress_port,
        #     None,
        # )

        # self.assertRaisesRegex(
        #     TypeError,
        #     "Invalid type for `ingress_port`: must be of type `Port`",
        #     connection.set_ingress_port,
        #     {},
        # )

        # self.assertRaisesRegex(
        #     ValueError,
        #     "Invalid value for `egress_port`: must not be `None`",
        #     connection.set_egress_port,
        #     None,
        # )

        # self.assertRaisesRegex(
        #     TypeError,
        #     "Invalid type for `egress_port`, must be of type `Port`",
        #     connection.set_egress_port,
        #     {},
        # )

    def test_connection_handler_no_ingress_port(self):
        connection_data = json.loads(
            TestData.CONNECTION_FILE_P2P_v0.read_text()
        )
        connection_data["ingress_port"] = None

        self.assertRaisesRegex(
            ValidationError,
            "1 validation error for ConnectionRequestV0",
            ConnectionRequestV0.model_validate,
            connection_data,
        )

    def test_connection_handler_no_egress_port(self):
        connection_data = json.loads(
            TestData.CONNECTION_FILE_P2P_v0.read_text()
        )
        connection_data["egress_port"] = None

        # self.assertRaisesRegex(
        #     MissingAttributeException,
        #     f"Missing required attribute 'egress_port' while parsing <{connection_data}>",
        #     ConnectionHandler().import_connection_data,
        #     connection_data,
        # )

        self.assertRaisesRegex(
            ValidationError,
            "1 validation error for ConnectionRequestV0",
            ConnectionRequestV0.model_validate,
            connection_data,
        )

    def test_import_connection_port_p2p_v2(self):
        """
        Test ConnectionHandler class for Port P2P Connection Request
        Spec v1.
        """
        connection_data = json.loads(
            TestData.CONNECTION_FILE_L2VPN_P2P_v1.read_text()
        )

        c = ConnectionRequestV1.model_validate(connection_data)
        self.assertIsInstance(c, ConnectionRequestV1)

        data = {
            "name": "new-connection",
            "endpoints": [
                {"port_id": "id1", "vlan": "777"},
                {"port_id": "id2"},
            ],
        }

        self.assertRaisesRegex(
            ValidationError,
            "1 validation error for ConnectionRequestV1",
            ConnectionRequestV1.model_validate,
            data,
        )


if __name__ == "__main__":
    unittest.main()
