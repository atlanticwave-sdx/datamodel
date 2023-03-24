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

    def setUp(self):
        self.handler = ConnectionHandler()  # noqa: E501

    def tearDown(self):
        pass

    def testImportConnection_p2p(self):
        connection = self.handler.import_connection(self.CONNECTION_FILE_P2P)
        self.assertIsInstance(connection, Connection)

    def testImportConnection_req(self):
        connection = self.handler.import_connection(self.CONNECTION_FILE_REQ)
        self.assertIsInstance(connection, Connection)

    def testImportConnection_MissingRequiredAttributes(self):
        """Exception expected when required attributes are missing."""
        self.assertRaises(
            MissingAttributeException, self.handler.import_connection_data, {}
        )
        self.assertRaises(
            MissingAttributeException,
            self.handler.import_connection_data,
            {"id": "id"},
        )
        self.assertRaises(
            MissingAttributeException,
            self.handler.import_connection_data,
            {"id": "id", "name": "name"},
        )
        self.assertRaises(
            MissingAttributeException,
            self.handler.import_connection_data,
            {"id": "id", "name": "name", "ingress_port": None},
        )
        self.assertRaises(
            MissingAttributeException,
            self.handler.import_connection_data,
            {"id": "id", "name": "name", "egress_port": None},
        )
        self.assertRaises(
            MissingAttributeException,
            self.handler.import_connection_data,
            {"id": "id", "egress_port": None, "ingress_port": None},
        )

    def testImportConnection_MissingOptionalAttributes(self):
        """No error expected when optional attributes are missing."""
        # All required attributes are set.
        ingress_port = {"id": "ingress_port_id", "name": "ingress_port_name"}
        egress_port = {"id": "egress_port_id", "name": "egress_port_name"}
        connection = self.handler.import_connection_data(
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
