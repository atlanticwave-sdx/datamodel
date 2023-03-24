import unittest

from sdx.datamodel.validation.connectionvalidator import ConnectionValidator
from sdx.datamodel.parsing.connectionhandler import ConnectionHandler

CONNECTION_P2P = "./tests/data/p2p.json"
# CONNECTION_P2P = './tests/data/test_connection.json'


class TestConnectionValidator(unittest.TestCase):
    def setUp(self):
        self.handler = ConnectionHandler()
        print("Import Connection:")
        self.handler.import_connection(CONNECTION_P2P)
        conn = self.handler.get_connection()
        self.validator = ConnectionValidator()
        self.validator.set_connection(conn)

    def tearDown(self):
        pass

    def testConnection(self):
        try:
            self.validator.is_valid()
            print(self.validator.get_connection())
        except DataModelException as e:
            print(e)
            return False
        return True


if __name__ == "__main__":
    unittest.main()
