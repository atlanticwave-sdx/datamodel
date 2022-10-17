import os
import unittest

from sdxdatamodel.models.connection import Connection
from sdxdatamodel.parsing.connectionhandler import ConnectionHandler
from sdxdatamodel.parsing.exceptions import DataModelException
from sdxdatamodel.validation.connectionvalidator import ConnectionValidator

# import parsing


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CONNECTION_P2P = os.path.join(TEST_DATA_DIR, "p2p.json")
CONNECTION_REQ = os.path.join(TEST_DATA_DIR, "test_request.json")


class TestConnectionValidator(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _get_validator(self, filename):
        """
        Return a validator for the given file.
        """
        handler = ConnectionHandler()
        conn = handler.import_connection(filename)

        validator = ConnectionValidator()
        validator.set_connection(conn)

        return validator

    def test_connection_json_p2p(self):
        """
        Validate a JSON document descibing a connection.
        """
        validator = self._get_validator(CONNECTION_P2P)
        self.assertTrue(validator.is_valid())

    def test_connection_json_req(self):
        """
        Validate a JSON document descibing a connection.
        """
        validator = self._get_validator(CONNECTION_REQ)
        self.assertTrue(validator.is_valid())


if __name__ == "__main__":
    unittest.main()
