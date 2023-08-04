import json
import unittest

from sdx.datamodel.models.port import Port
from sdx.datamodel.parsing.exceptions import InvalidVlanRangeException
from sdx.datamodel.parsing.porthandler import PortHandler

from . import TestData


class PortHandlerTests(unittest.TestCase):
    """
    Tests for port data parsing logic.
    """

    def test_import_port_json(self):
        """
        Test that a Port object can be created given a JSON
        descritpion of a port.
        """
        self.assertIsInstance(
            PortHandler().import_port(TestData.PORT_FILE), Port
        )

    def test_import_port_json_l2vpn_ptp(self):
        """
        Test that a Port object can be created given a JSON
        descritpion of a port.
        """
        self.assertIsInstance(
            PortHandler().import_port(TestData.PORT_FILE_L2VPN_PTP), Port
        )

    def test_import_port_json_l2vpn_ptp_invalid(self):
        """
        Test that a Port object cannot be created given an incorrect
        JSON descritpion of a port.
        """
        self.assertRaises(
            json.decoder.JSONDecodeError,
            PortHandler().import_port,
            TestData.PORT_FILE_L2VPN_PTP_INVALID,
        )

    def test_import_port_json_l2vpn_ptp_bad_range(self):
        """
        Test that a Port object cannot be created with a range
        like [n1, n2], where n1 > n2.
        """
        self.assertRaises(
            InvalidVlanRangeException,
            PortHandler().import_port,
            TestData.PORT_FILE_L2VPN_PTP_BAD_RANGE,
        )

    def test_import_port_json_l2vpn_ptp_and_ptmp(self):
        """
        Test that a Port object cannot be created given an incorrect
        JSON descritpion of a port.
        """
        self.assertIsInstance(
            PortHandler().import_port(TestData.PORT_FILE_L2VPN_PTP_PTMP), Port
        )

    def test_import_port_json_l2vpn_ptp_and_ptmp_invalid(self):
        """
        Test that a Port object cannot be be created given a JSON
        descritpion of a port.
        """
        self.assertRaises(
            json.decoder.JSONDecodeError,
            PortHandler().import_port,
            TestData.PORT_FILE_L2VPN_PTP_PTMP_INVALID,
        )


if __name__ == "__main__":
    unittest.main()
