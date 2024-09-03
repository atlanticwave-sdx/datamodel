import unittest
import json

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


if __name__ == "__main__":
    unittest.main()
