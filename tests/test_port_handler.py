import json
import unittest

from sdx_datamodel.models.port import Port
from sdx_datamodel.parsing.exceptions import (
    InvalidVlanRangeException,
    MissingAttributeException,
)
from sdx_datamodel.parsing.porthandler import PortHandler

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

    def test_import_port_data(self):
        """Test import_port_data function."""
        self.assertIsInstance(
            PortHandler().import_port_data({"id": "1", "name": "a"}), Port
        )
        with self.assertRaises(MissingAttributeException) as ex:
            PortHandler().import_port_data({})

    def test_validate_services_vlan_range(self):
        """Test import_port_data function."""
        vlan_range = [1, [10, 100], [300, 400]]
        data = {
            "id": "1",
            "name": "a",
            "services": {"l2vpn-ptp": {"vlan_range": vlan_range}},
        }
        self.assertIsInstance(PortHandler().import_port_data(data), Port)

        vlan_range[0] = [1, 2, 3]
        with self.assertRaises(InvalidVlanRangeException) as ex:
            PortHandler().import_port_data(data)

        vlan_range[0] = [1, "2"]
        with self.assertRaises(InvalidVlanRangeException) as ex:
            PortHandler().import_port_data(data)

        data["services"].pop("l2vpn-ptp")
        data["services"]["l2vpn-ptmp"] = {"vlan_range": None}
        with self.assertRaises(InvalidVlanRangeException) as ex:
            PortHandler().import_port_data(data)

    def test_port_setters(self):
        port = PortHandler().import_port(TestData.PORT_FILE)
        self.assertIsInstance(port, Port)

        with self.assertRaises(ValueError) as ex:
            port.name = None

        self.assertIn(
            "Invalid value for `name`, must not be `None`", ex.exception.args
        )

        with self.assertRaises(ValueError) as ex:
            port.id = None

        self.assertIn(
            "Invalid value for `id`, must not be `None`", ex.exception.args
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
