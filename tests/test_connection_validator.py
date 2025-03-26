import datetime
import unittest

import json

from sdx_datamodel.models.connection_request import ConnectionRequest
from sdx_datamodel.models.port import Port
from sdx_datamodel.parsing.connectionhandler import ConnectionHandler
from sdx_datamodel.parsing.exceptions import (
    AttributeNotSupportedException,
    ServiceNotSupportedException,
)
# from sdx_datamodel.validation.connectionvalidator import ConnectionValidator
from sdx_datamodel.models.connection_request import ConnectionRequest

from . import TestData


class ConnectionValidatorTests(unittest.TestCase):
    """
    Tests for ConnectionValidator class.
    """

    def _get_validator(self, path):
        """
        Return a validator for the given file.
        """
        # handler = ConnectionHandler()
        # connection = handler.import_connection(path)
        data = json.loads(path.read_text())
        return ConnectionRequest(data)

    def test_connection_json_p2p(self):
        """
        Validate a JSON document descibing a connection.
        """
        validator = self._get_validator(TestData.CONNECTION_FILE_P2P_v0)
        self.assertTrue(validator.is_valid())

    def test_connection_json_req(self):
        """
        Validate a JSON document descibing a connection.
        """
        validator = self._get_validator(TestData.CONNECTION_FILE_REQ_v0)
        self.assertTrue(validator.is_valid())

    def test_connection_json_req_no_node(self):
        """
        Validate a JSON document descibing a "node-less" connection.
        """
        validator = self._get_validator(
            TestData.CONNECTION_FILE_REQ_NO_NODE_v0
        )
        self.assertTrue(validator.is_valid())

    def test_connection_json_req_bad_name(self):
        """
        Connection name must be a string.
        """
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_REQ_v0
        )
        connection.name = 42

        with self.assertRaises(ValueError) as ex:
            ConnectionValidator(connection).is_valid()

        self.assertIn("Connection 42 name must be a string", ex.exception.args)

    def test_connection_json_req_bad_id(self):
        """
        Connection ID must be a string.
        """
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_REQ_v0
        )
        connection.id = 42

        with self.assertRaises(ValueError) as ex:
            ConnectionValidator(connection).is_valid()

        self.assertIn("Connection ID must be a string", ex.exception.args)

    def test_connection_json_req_bad_ports(self):
        """
        Ingress and egress ports must have valid names and IDs.
        """
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_REQ_v0
        )

        connection.ingress_port.name = 32
        connection.ingress_port.id = 32

        connection.egress_port.name = 42
        connection.egress_port.id = 42
        connection.egress_port.vlan_range = None

        print(f"connection = {connection}")

        with self.assertRaises(ValueError) as ex:
            ConnectionValidator(connection).is_valid()

        errors = ex.exception.args[0].splitlines()

        self.assertEqual(
            errors,
            [
                "Port ID must be a string",
                "Port 32 name must be a string",
                "Port ID must be a string",
                "Port 42 name must be a string",
                "Port 42 must have a vlan",
            ],
        )

    def test_connection_object(self):
        """
        Create a connection object and validate it.
        """
        ingress_port = Port(
            id="ingress_port_id",
            name="ingress_port_name",
            node="ingress_node_name",
            vlan_range="100",
            status="unknown",
        )

        egress_port = Port(
            id="egress_port_id",
            name="egress_port_name",
            node="egress_node_name",
            vlan_range="100",
            status="unknown",
        )

        connection = ConnectionRequest(
            id="test_place_connection_id",
            name="test_place_connection_name",
            ingress_port=ingress_port,
            egress_port=egress_port,
            quantity=0,
            start_time=str(
                datetime.datetime.now() + datetime.timedelta(seconds=100)
            ),
            status="fail",
            complete=False,
        )

        self.assertIsInstance(connection, ConnectionRequest)

    def test_connection_object_invalid(self):
        """
        Create a connection object and validate it.
        """
        ingress_port = Port(
            id="ingress_port_id",
            name="ingress_port_name",
            node="ingress_node_name",
            vlan_range="100",
            status="unknown",
        )

        egress_port = Port(
            id="egress_port_id",
            name="egress_port_name",
            node="egress_node_name",
            vlan_range="5000",
            status="unknown",
        )

        connection = ConnectionRequest(
            id="test_place_connection_id",
            name="test_place_connection_name",
            ingress_port=ingress_port,
            egress_port=egress_port,
            quantity=0,
            status="fail",
            complete=False,
        )

        self.assertIsInstance(connection, ConnectionRequest)

        with self.assertRaises(ValueError) as ex:
            validator = ConnectionValidator(connection).is_valid()
        print(f"ex = {ex.exception.args}")
        self.assertIn(
            "VLAN range 5000 is invalid: 5000 is out of range (1-4095)",
            ex.exception.args[0],
        )

    def test_validate_vlan_valid(self):
        """
        Test _validate_vlan with a valid VLAN range.
        """
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_REQ_v0
        )
        connection.egress_port.vlan_range = "100-200"
        validator = ConnectionValidator(connection)
        self.assertTrue(
            validator._validate_vlan(connection.egress_port.vlan_range)
        )

    def test_validate_vlan_invalid(self):
        """
        Test _validate_vlan with an invalid VLAN range.
        """
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_REQ_v0
        )
        connection.egress_port.vlan_range = "5000"
        validator = ConnectionValidator(connection)
        error = validator._validate_vlan(connection.egress_port.vlan_range)
        self.assertIn(
            "VLAN range 5000 is invalid: 5000 is out of range (1-4095)",
            error,
        )

    def test_validate_vlan_invalid_range(self):
        """
        Test _validate_vlan with an invalid VLAN range format.
        """
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_REQ_v0
        )
        connection.egress_port.vlan_range = "200:100"
        validator = ConnectionValidator(connection)
        error = validator._validate_vlan(connection.egress_port.vlan_range)
        self.assertIn(
            "VLAN range 200:100 is invalid: 200 > 100",
            error,
        )

    def test_connection_validator_null_input(self):
        # Expect the matched error message when input is null.
        self.assertRaisesRegex(
            ValueError,
            "ConnectionValidator must be passed a Connection object",
            ConnectionValidator,
            None,
        )

    def test_connection_validator_empty_input(self):
        # Expect the matched error message when input is empty.
        self.assertRaisesRegex(
            ValueError,
            "ConnectionValidator must be passed a Connection object",
            ConnectionValidator,
            {},
        )

    def test_validate_time_valid(self):
        """
        Test _validate_time with a valid time range.
        """
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_REQ_v0
        )
        connection.start_time = str(
            datetime.datetime.now() + datetime.timedelta(seconds=100)
        )
        validator = ConnectionValidator(connection)
        error = validator._validate_time(
            connection.start_time, connection.end_time, connection
        )
        self.assertTrue(len(error) == 0)

    def test_validate_time_invalid_format(self):
        """
        Test _validate_time with an invalid time format.
        """
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_REQ_v0
        )
        connection.start_time = "invalid_time_format"
        validator = ConnectionValidator(connection)
        error = validator._validate_time(
            connection.start_time, connection.end_time, connection
        )
        self.assertIn(
            "Scheduling not possible",
            error[0],
        )

    def test_validate_time_past_time(self):
        """
        Test _validate_time with a past time.
        """
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_REQ_v0
        )
        connection.start_time = str(
            datetime.datetime.now() - datetime.timedelta(days=1)
        )
        validator = ConnectionValidator(connection)
        error = validator._validate_time(
            connection.start_time, connection.end_time, connection
        )
        self.assertIn(
            "Scheduling not possible",
            error[0],
        )

    def test_start_time_too_far_in_future(self):
        """
        Test start_time that is too far in the future.
        """
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_REQ_v0
        )
        connection.start_time = str(
            datetime.datetime.now() + datetime.timedelta(seconds=600)
        )
        validator = ConnectionValidator(connection)

        with self.assertRaises(AttributeNotSupportedException) as ex:
            validator.is_valid()

        self.assertIn(
            "Scheduling advanced reservation is not supported: start_time",
            ex.exception.args[0],
        )

    def test_attribute_not_supported_exception(self):
        """
        Test for AttributeNotSupportedException.
        """
        connection = ConnectionHandler().import_connection(
            TestData.CONNECTION_FILE_REQ_v0
        )

        connection.end_time = str(
            datetime.datetime.now() + datetime.timedelta(days=1)
        )
        validator = ConnectionValidator(connection)

        with self.assertRaises(AttributeNotSupportedException) as ex:
            validator.is_valid()

        self.assertIn(
            "Scheduling advanced reservation is not supported: end_time",
            ex.exception.args[0],
        )


if __name__ == "__main__":
    unittest.main()
