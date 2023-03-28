import pathlib
import unittest

from sdx.datamodel.models.port import Port
from sdx.datamodel.parsing.porthandler import PortHandler


class PortHandlerTests(unittest.TestCase):
    TEST_DATA_DIR = pathlib.Path(__file__).parent.joinpath("data")
    PORT_DATA_FILE = TEST_DATA_DIR.joinpath("port.json")

    def test_import_port_json(self):
        """
        Test that a Port object can be created given a JSON descritpion of a port.
        """
        handler = PortHandler()

        # import_port() must not raise a DataModelException.
        port = handler.import_port(self.PORT_DATA_FILE)
        self.assertIsInstance(port, Port)


if __name__ == "__main__":
    unittest.main()
