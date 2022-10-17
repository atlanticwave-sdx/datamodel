import os
import unittest


from sdxdatamodel.parsing.porthandler import PortHandler
from sdxdatamodel.parsing.exceptions import DataModelException

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PORT_DATA = os.path.join(TEST_DATA_DIR, "port.json")


class TestPortHandler(unittest.TestCase):
    def setUp(self):
        self.handler = PortHandler()  # noqa: E501

    def tearDown(self):
        pass

    def testImportPort(self):
        try:
            print("Test Port")
            self.handler.import_port(PORT_DATA)
            print(self.handler.port)
        except DataModelException as e:
            print(e)
            return False
        return True


if __name__ == "__main__":
    unittest.main()
