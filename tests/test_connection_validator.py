import os
import unittest

# import parsing

from sdxdatamodel.validation.connectionvalidator import ConnectionValidator
from sdxdatamodel.parsing.connectionhandler import ConnectionHandler
from sdxdatamodel.parsing.exceptions import DataModelException
from sdxdatamodel.models.connection import Connection

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CONNECTION_P2P = os.path.join(TEST_DATA_DIR, "p2p.json")
# CONNECTION_P2P = './tests/data/test_connection.json'


class TestConnectionValidator(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_connection_json(self):
        """
        Test that a JSON document that describes a connection can be
        validated.
        """
        handler = ConnectionHandler()
        conn = handler.import_connection(CONNECTION_P2P)

        validator = ConnectionValidator()
        validator.set_connection(conn)

        self.assertTrue(validator.is_valid())


if __name__ == "__main__":
    unittest.main()
