import datetime
import unittest

from sdx.datamodel.models.connection import Connection
from sdx.datamodel.models.port import Port
from sdx.datamodel.parsing.connectionhandler import ConnectionHandler
from sdx.datamodel.validation.connectionvalidator import ConnectionValidator

from . import TestData


class ConnectionValidatorTests(unittest.TestCase):
    """
    Tests for ConnectionValidator class.
    """

    def _get_validator(self, path):
        """
        Return a validator for the given file.
        """
        handler = ConnectionHandler()
        connection = handler.import_connection(path)
        return ConnectionValidator(connection)

    def test_connection_json_p2p(self):
        """
        Validate a JSON document descibing a connection.
        """
        validator = self._get_validator(TestData.CONNECTION_FILE_P2P)
        self.assertTrue(validator.is_valid())

    def test_connection_json_req(self):
        """
        Validate a JSON document descibing a connection.
        """
        validator = self._get_validator(TestData.CONNECTION_FILE_REQ)
        self.assertTrue(validator.is_valid())

    def test_connection_object(self):
        """
        Create a connection object and validate it.
        """
        ingress_port = Port(
            id="ingress_port_id",
            name="ingress_port_name",
            node="ingress_node_name",
            status="unknown",
        )

        egress_port = Port(
            id="egress_port_id",
            name="egress_port_name",
            node="egress_node_name",
            status="unknown",
        )

        connection = Connection(
            id="test_place_connection_id",
            name="test_place_connection_name",
            ingress_port=ingress_port,
            egress_port=egress_port,
            quantity=0,
            start_time=datetime.datetime.fromtimestamp(0),
            end_time=datetime.datetime.fromtimestamp(0),
            status="fail",
            complete=False,
        )

        self.assertIsInstance(connection, Connection)

        validator = ConnectionValidator(connection)
        self.assertTrue(validator.is_valid())

    def test_connection_validator_null_input(self):
        # Expect the matched error message when input is null.
        self.assertRaisesRegex(
            ValueError,
            "ConnectionValidator must be passed a Connection object",
            ConnectionValidator,
            None,
        )


if __name__ == "__main__":
    unittest.main()
