import unittest

from sdx.datamodel.models.port import Port
from sdx.datamodel.parsing.porthandler import PortHandler

from . import TestData


class PortHandlerTests(unittest.TestCase):
    def test_import_port_json(self):
        """
        Test that a Port object can be created given a JSON descritpion of a port.
        """
        handler = PortHandler()

        # import_port() must not raise a DataModelException.
        port = handler.import_port(TestData.PORT_FILE)
        self.assertIsInstance(port, Port)


if __name__ == "__main__":
    unittest.main()
