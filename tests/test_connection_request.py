import json
import unittest

from pydantic import ValidationError

from sdx_datamodel.models.connection_request import ConnectionRequestV1

from . import TestData


class TestConnectionRequestV1(unittest.TestCase):

    def test_basic_connection_request(self):
        testdata = json.loads(
            TestData.CONNECTION_FILE_L2VPN_VLAN_TRANS_V1.read_text()
        )
        request = ConnectionRequestV1(**testdata)

        self.assertEqual(request.name, "VLAN between AMPATH/300 and TENET/150")

        self.assertEqual(len(request.endpoints), 2)

        self.assertEqual(
            request.endpoints[0].port_id, "urn:sdx:port:tenet.ac.za:Tenet03:50"
        )
        self.assertEqual(request.endpoints[0].vlan, "150")

        self.assertEqual(
            request.endpoints[1].port_id, "urn:sdx:port:ampath.net:Ampath3:50"
        )
        self.assertEqual(request.endpoints[1].vlan, "300")

    def test_vlan_not_string(self):
        testdata = {
            "name": "Bad connection request: vlan must be string",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:tenet.ac.za:Tenet03:50",
                    "vlan": 100,
                },
                {
                    "port_id": "urn:sdx:port:ampath.net:Ampath3:50",
                    "vlan": 100.0,
                },
            ],
        }

        # Both VLANs are not strings; expect two validation errors.
        self.assertRaisesRegex(
            ValidationError,
            "2 validation errors for ConnectionRequestV1",
            ConnectionRequestV1,
            **testdata,
        )


if __name__ == "__main__":
    unittest.main()
