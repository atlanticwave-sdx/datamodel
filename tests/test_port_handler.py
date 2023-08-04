import json
import unittest

from sdx.datamodel.models.port import Port
from sdx.datamodel.parsing.porthandler import PortHandler

from . import TestData


class PortHandlerTests(unittest.TestCase):
    """
    Tests for port data parsing logic.
    """

    def test_import_port_json(self):
        """
        Test that a Port object can be created given a JSON descritpion of a port.
        """
        handler = PortHandler()

        # import_port() must not raise a DataModelException.
        port = handler.import_port(TestData.PORT_FILE)
        self.assertIsInstance(port, Port)

    def test_import_port_json_l2vpn_ptp(self):
        """
        Test that a Port object can be created given a JSON descritpion of a port.
        """
        handler = PortHandler()

        # import_port() must not raise a DataModelException.
        port = handler.import_port(TestData.PORT_FILE_L2VPN_PTP)
        self.assertIsInstance(port, Port)

    def test_import_port_json_l2vpn_ptp_bad(self):
        """
        Test that a Port object can be created given a JSON descritpion of a port.
        """
        self.assertRaises(
            json.decoder.JSONDecodeError,
            PortHandler().import_port,
            TestData.PORT_FILE_L2VPN_PTP_BAD
        )

    def test_import_port_json_l2vpn_ptp_and_ptmp(self):
        """
        Test that a Port object can be created given a JSON descritpion of a port.
        """
        handler = PortHandler()

        # import_port() must not raise a DataModelException.
        port = handler.import_port(TestData.PORT_FILE_L2VPN_PTP_PTMP)
        self.assertIsInstance(port, Port)

    def test_import_port_json_l2vpn_ptp_and_ptmp_bad(self):
        """
        Test that a Port object can be created given a JSON descritpion of a port.
        """
        self.assertRaises(
            json.decoder.JSONDecodeError,
            PortHandler().import_port,
            TestData.PORT_FILE_L2VPN_PTP_PTMP_BAD,
        )


if __name__ == "__main__":
    unittest.main()
