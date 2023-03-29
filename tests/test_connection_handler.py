import pathlib
import unittest

from sdx.datamodel.models.connection import Connection
from sdx.datamodel.parsing.connectionhandler import ConnectionHandler
from sdx.datamodel.parsing.exceptions import MissingAttributeException


class TestConnectionHandler(unittest.TestCase):
    """Test ConnectionHandler class."""

    TEST_DATA_DIR = pathlib.Path(__file__).parent.joinpath("data")
    CONNECTION_FILE_P2P = TEST_DATA_DIR.joinpath("p2p.json")
    CONNECTION_FILE_REQ = TEST_DATA_DIR.joinpath("test_request.json")

    def test_import_connection_p2p(self):
        connection = ConnectionHandler().import_connection(
            self.CONNECTION_FILE_P2P
        )
        self.assertIsInstance(connection, Connection)

    def test_import_connection_req(self):
        connection = ConnectionHandler().import_connection(
            self.CONNECTION_FILE_REQ
        )
        self.assertIsInstance(connection, Connection)

    def test_import_connection_MissingRequiredAttributes(self):
        """Exception expected when required attributes are missing."""
        data = {}
        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing attribute 'id' while parsing <{data}>",
            ConnectionHandler().import_connection_data,
            data,
        )

        data = {"id": "id"}
        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing attribute 'name' while parsing <{data}>",
            ConnectionHandler().import_connection_data,
            data,
        )

        data = {"id": "id", "name": "name"}
        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing attribute 'ingress_port' while parsing <{data}>",
            ConnectionHandler().import_connection_data,
            data,
        )

        data = {"id": "id", "name": "name", "ingress_port": None}
        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing attribute 'ingress_port' while parsing <{data}>",
            ConnectionHandler().import_connection_data,
            data,
        )

        data = {"id": "id", "name": "name", "egress_port": None}
        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing attribute 'ingress_port' while parsing <{data}>",
            ConnectionHandler().import_connection_data,
            data,
        )

        data = {"id": "id", "egress_port": None, "ingress_port": None}
        self.assertRaisesRegex(
            MissingAttributeException,
            f"Missing attribute 'name' while parsing <{data}>",
            ConnectionHandler().import_connection_data,
            data,
        )

    def test_import_connection_MissingOptionalAttributes(self):
        """No error expected when optional attributes are missing."""
        # All required attributes are set.
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


if __name__ == "__main__":
    unittest.main()
