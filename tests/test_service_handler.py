import unittest

from sdx.datamodel.parsing.exceptions import DataModelException
from sdx.datamodel.parsing.servicehandler import ServiceHandler

service = "./tests/data/service.json"


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


if __name__ == "__main__":
    unittest.main()
