import unittest

import parsing

from parsing.servicehandler import ServiceHandler
from parsing.exceptions import DataModelException

service = './test/data/service.json'

class TestServiceHandler(unittest.TestCase):

    def setUp(self):
        self.handler = ServiceHandler()  # noqa: E501
    def tearDown(self):
        pass

    def testImportService(self):
        try:
            print("Test Service")
            self.handler.import_service(service)
            print(self.handler.service)
        except DataModelException as e:
            print(e)
            return False      
        return True

if __name__ == '__main__':
    unittest.main()