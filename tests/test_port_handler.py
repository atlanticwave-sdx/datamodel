import os
import unittest

from sdx.datamodel.models.port import Port
from sdx.datamodel.parsing.exceptions import DataModelException
from sdx.datamodel.parsing.porthandler import PortHandler


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PORT_DATA = os.path.join(TEST_DATA_DIR, "port.json")


class TestPortHandler(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_import_port_json(self):
        """
        Test that a Port object can be created given a JSON descritpion of a port.
        """
        handler = PortHandler()
        # import_port() must not raise a DataModelException.
        port = handler.import_port(PORT_DATA)
        self.assertIsInstance(port, Port)


if __name__ == "__main__":
    unittest.main()
