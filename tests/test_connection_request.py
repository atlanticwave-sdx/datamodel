import datetime
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

    def test_connection_request_empty(self):
        testdata = {}

        self.assertRaisesRegex(
            ValidationError,
            "2 validation errors for ConnectionRequestV1",
            ConnectionRequestV1,
            **testdata,
        )

    def test_connection_request_no_endpoints(self):
        testdata = {
            "name": "no-endpoints",
        }

        self.assertRaisesRegex(
            ValidationError,
            "1 validation error for ConnectionRequestV1",
            ConnectionRequestV1,
            **testdata,
        )

    def test_connection_request_empty_endpoints(self):
        testdata = {
            "name": "no-endpoints",
            "endpoints": [],
        }

        self.assertRaisesRegex(
            ValidationError,
            "1 validation error for ConnectionRequestV1",
            ConnectionRequestV1,
            **testdata,
        )

    def test_connection_request_one_endpoint(self):
        testdata = {
            "name": "no-endpoints",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:example.net:p:1",
                    "vlan": "-1",
                },
            ],
        }

        self.assertRaisesRegex(
            ValidationError,
            "1 validation error for ConnectionRequestV1",
            ConnectionRequestV1,
            **testdata,
        )

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

    def test_vlan_in_invalid_number(self):
        testdata = {
            "name": "Bad connection request: vlan must be in [1,4095] range",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:example.net:p:1",
                    "vlan": "-1",
                },
                {
                    "port_id": "urn:sdx:port:example.net:p:2",
                    "vlan": "5000",
                },
            ],
        }

        # Both VLANs are not in the [1,4095] range; expect two
        # validation errors.
        self.assertRaisesRegex(
            ValidationError,
            "2 validation errors for ConnectionRequestV1",
            ConnectionRequestV1,
            **testdata,
        )

    def test_vlan_in_invalid_range(self):
        testdata = {
            "name": "Bad connection request: vlan must be in [1,4095] range",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:example.net:p:1",
                    "vlan": "100:not-a-number",
                },
                {
                    "port_id": "urn:sdx:port:example.net:p:2",
                    "vlan": "200:100",
                },
            ],
        }

        # Both VLANs are not in the [1,4095] range; expect two
        # validation errors.
        self.assertRaisesRegex(
            ValidationError,
            "2 validation errors for ConnectionRequestV1",
            ConnectionRequestV1,
            **testdata,
        )

    def test_vlan_in_valid_range(self):
        request_name = "Connection request with valid vlan ranges"
        port0_id = "urn:sdx:port:example.net:p:1"
        port0_vlan = "100:200"
        port1_id = "urn:sdx:port:example.net:p:2"
        port1_vlan = "200:300"
        testdata = {
            "name": request_name,
            "endpoints": [
                {
                    "port_id": port0_id,
                    "vlan": port0_vlan,
                },
                {
                    "port_id": port1_id,
                    "vlan": port1_vlan,
                },
            ],
        }

        request = ConnectionRequestV1(**testdata)
        self.assertEqual(request.name, request_name)
        self.assertEqual(request.endpoints[0].port_id, port0_id)
        self.assertEqual(request.endpoints[0].vlan, port0_vlan)
        self.assertEqual(request.endpoints[1].port_id, port1_id)
        self.assertEqual(request.endpoints[1].vlan, port1_vlan)

    def test_connection_request_with_optional_fields(self):
        testdata = json.loads(
            TestData.CONNECTION_FILE_L2VPN_P2P_V1.read_text()
        )
        request = ConnectionRequestV1(**testdata)

        self.assertEqual(request.name, "new-connection")
        self.assertEqual(request.description, "a test circuit")

        self.assertEqual(len(request.endpoints), 2)

        self.assertIsInstance(
            request.scheduling.start_time,
            datetime.datetime,
        )
        self.assertIsInstance(
            request.scheduling.start_time,
            datetime.datetime,
        )

        # self.assertEqual(
        #     request.scheduling.start_time,
        #     datetime.datetime(2024, 6, 24, 1, 0, tzinfo=TzInfo(UTC)),
        # )
        # self.assertEqual(
        #     request.scheduling.start_time,
        #     datetime.datetime(2024, 6, 26, 1, 0, tzinfo=TzInfo(UTC)),
        # )

        self.assertEqual(request.qos_metrics.min_bw.value, 12)
        self.assertEqual(request.qos_metrics.min_bw.strict, True)

        self.assertEqual(request.qos_metrics.max_delay.value, 4)
        self.assertEqual(request.qos_metrics.max_delay.strict, False)

        self.assertEqual(request.qos_metrics.max_number_oxps.value, 7)
        self.assertEqual(request.qos_metrics.max_number_oxps.strict, True)


if __name__ == "__main__":
    unittest.main()
