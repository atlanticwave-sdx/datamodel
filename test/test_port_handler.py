import unittest

import parsing

from parsing.porthandler import PortHandler
from parsing.exceptions import DataModelException

port = './test/data/port.json'

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

if __name__ == '__main__':
    unittest.main()