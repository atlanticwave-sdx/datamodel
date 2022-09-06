import unittest

# import parsing
import os

from sdxdatamodel.parsing.connectionhandler import ConnectionHandler
from sdxdatamodel.parsing.exceptions import DataModelException

# Test data is present inside current module's directory.
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CONNECTION_FILE_P2P = os.path.join(TEST_DATA_DIR, "p2p.json")
CONNECTION_FILE_REQ = os.path.join(TEST_DATA_DIR, "test_request.json")

class TestConnectionHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ConnectionHandler()  # noqa: E501

    def tearDown(self):
        pass

    def testImportConnection_p2p(self):
        try:
            print("Test Connection")
            self.handler.import_connection(CONNECTION_FILE_P2P)
            print(self.handler.connection)
        except DataModelException as e:
            print(e)
            return False
        return True


if __name__ == "__main__":
    unittest.main()
