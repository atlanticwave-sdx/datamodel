import os
import unittest

from sdxdatamodel.models.connection import Connection
from sdxdatamodel.parsing.connectionhandler import ConnectionHandler
from sdxdatamodel.parsing.exceptions import MissingAttributeException

# Test data is present inside current module's directory.
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CONNECTION_FILE_P2P = os.path.join(TEST_DATA_DIR, "p2p.json")
CONNECTION_FILE_REQ = os.path.join(TEST_DATA_DIR, "test_request.json")


class TestConnectionHandler(unittest.TestCase):
    """Test ConnectionHandler class."""

    def setUp(self):
        self.handler = ConnectionHandler()  # noqa: E501

    def tearDown(self):
        pass

    def testImportConnection_p2p(self):
        connection = self.handler.import_connection(CONNECTION_FILE_P2P)
        self.assertIsInstance(connection, Connection)

    def testImportConnection_req(self):
        connection = self.handler.import_connection(CONNECTION_FILE_REQ)
        self.assertIsInstance(connection, Connection)

    def testImportConnection_MissingRequiredAttributes(self):
        """Exception expected when required attributes are missing."""
        self.assertRaises(
            MissingAttributeException, self.handler.import_connection_data, {}
        )
        self.assertRaises(
            MissingAttributeException, self.handler.import_connection_data,
            {"id": "id"}
        )
        self.assertRaises(
            MissingAttributeException,
            self.handler.import_connection_data,
            {"id": "id", "name": "name"},
        )
        self.assertRaises(
            MissingAttributeException,
            self.handler.import_connection_data,
            {"id": "id", "name": "name", "ingress_port": []},
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
