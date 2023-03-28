import datetime
import json
import pathlib
import unittest

from sdx.datamodel.models.connection import Connection
from sdx.datamodel.models.port import Port
from sdx.datamodel.parsing.exceptions import MissingAttributeException
from sdx.datamodel.parsing.connectionhandler import ConnectionHandler
from sdx.datamodel.validation.connectionvalidator import ConnectionValidator


class ConnectionValidatorTests(unittest.TestCase):
    """
    Tests for ConnectionValidator class.
    """

    TEST_DATA_DIR = pathlib.Path(__file__).parent.joinpath("data")
    CONNECTION_P2P = TEST_DATA_DIR.joinpath("p2p.json")
    CONNECTION_REQ = TEST_DATA_DIR.joinpath("test_request.json")

    def _get_validator(self, path):
        """
        Return a validator for the given file.
        """
        handler = ConnectionHandler()
        connection = handler.import_connection(path)

        validator = ConnectionValidator()
        validator.set_connection(connection)

        return validator

    def test_connection_json_p2p(self):
        """
        Validate a JSON document descibing a connection.
        """
        validator = self._get_validator(self.CONNECTION_P2P)
        self.assertTrue(validator.is_valid())

    def test_connection_json_req(self):
        """
        Validate a JSON document descibing a connection.
        """
        validator = self._get_validator(self.CONNECTION_REQ)
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

        validator = ConnectionValidator()
        validator.set_connection(connection)
        self.assertTrue(validator.is_valid())

    def test_connection_validator_null_input(self):
        # Expect the matched error message when input is null.
        self.assertRaisesRegex(
            ValueError,
            "The Validator must be passed a Connection object",
            ConnectionValidator().set_connection,
            None,
        )

    def test_connection_handler_no_ingress_port(self):
        with open(self.CONNECTION_P2P, "r", encoding="utf-8") as f:
            connection_data = json.load(f)

        connection_data["ingress_port"] = None

        self.assertRaisesRegex(
            MissingAttributeException,
            "Missing attribute ingress_port must not be None while parsing <ingress_port>",
            ConnectionHandler().import_connection_data,
            connection_data,
        )

    def test_connection_handler_no_egress_port(self):
        with open(self.CONNECTION_P2P, "r", encoding="utf-8") as f:
            connection_data = json.load(f)

        connection_data["egress_port"] = None

        self.assertRaisesRegex(
            MissingAttributeException,
            "Missing attribute egress_port must not be None while parsing <egress_port>",
            ConnectionHandler().import_connection_data,
            connection_data,
        )


if __name__ == "__main__":
    unittest.main()
