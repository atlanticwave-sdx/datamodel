import unittest

from sdx.datamodel.parsing.exceptions import DataModelException
from sdx.datamodel.parsing.porthandler import PortHandler

port = "./tests/data/port.json"


class TestPortHandler(unittest.TestCase):
    def setUp(self):
        self.handler = PortHandler()  # noqa: E501

    def tearDown(self):
        pass

    def testImportPort(self):
        try:
            print("Test Port")
            self.handler.import_port(port)
            print(self.handler.port)
        except DataModelException as e:
            print(e)
            return False
        return True


if __name__ == "__main__":
    unittest.main()
