import datetime
import json
import unittest

from pydantic import ValidationError

from sdx_datamodel.models.connection_request import ConnectionRequestV1

from . import TestData


class TestConnectionRequestV1(unittest.TestCase):
    def test_basic_connection_request(self):
        """
        Test a basic connection request.
        """
        request = ConnectionRequestV1.parse_file(
            TestData.CONNECTION_FILE_L2VPN_VLAN_TRANS_V1
        )

        self.assertIsInstance(request, ConnectionRequestV1)

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

    def test_connection_request_vlan_not_string(self):
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

    def test_connection_request_vlan_invalid_number(self):
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

    def test_connection_request_vlan_invalid_range(self):
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

    def test_connection_request_vlan_invalid_integers_in_range(self):
        testdata = {
            "name": "Bad connection request: vlan must be in [1,4095] range",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:example.net:p:1",
                    "vlan": "1:10000",
                },
                {
                    "port_id": "urn:sdx:port:example.net:p:2",
                    "vlan": "10000:1",
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

    def test_connection_request_vlan_invalid_strings_in_range(self):
        testdata = {
            "name": "Bad connection request: vlan must be in [1,4095] range",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:example.net:p:1",
                    "vlan": "1:10000",
                },
                {
                    "port_id": "urn:sdx:port:example.net:p:2",
                    "vlan": "10000:any",
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

    def test_connection_request_vlan_all_all(self):
        testdata = {
            "name": "Bad connection request: vlan must be in [1,4095] range",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:example.net:p:1",
                    "vlan": "all",
                },
                {
                    "port_id": "urn:sdx:port:example.net:p:2",
                    "vlan": "all",
                },
            ],
        }

        request = ConnectionRequestV1(**testdata)

        self.assertEqual(request.endpoints[0].vlan, "all")
        self.assertEqual(request.endpoints[1].vlan, "all")

    def test_connection_request_vlan_any_any(self):
        testdata = {
            "name": "Bad connection request: vlan must be in [1,4095] range",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:example.net:p:1",
                    "vlan": "any",
                },
                {
                    "port_id": "urn:sdx:port:example.net:p:2",
                    "vlan": "any",
                },
            ],
        }

        request = ConnectionRequestV1(**testdata)

        self.assertEqual(request.endpoints[0].vlan, "any")
        self.assertEqual(request.endpoints[1].vlan, "any")

    def test_connection_request_vlan_invalid_strings(self):
        testdata = {
            "name": "Bad connection request: vlan must be in [1,4095] range",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:example.net:p:1",
                    "vlan": "unknown",
                },
                {
                    "port_id": "urn:sdx:port:example.net:p:2",
                    "vlan": "random",
                },
            ],
        }

        # Both VLANs are not any of the expected strings; expect two
        # validation errors.
        self.assertRaisesRegex(
            ValidationError,
            "2 validation errors for ConnectionRequestV1",
            ConnectionRequestV1,
            **testdata,
        )

    def test_connection_request_vlan_valid_range(self):
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
        """
        Test a connection request that has optional fields.
        """
        request = ConnectionRequestV1.parse_file(
            TestData.CONNECTION_FILE_L2VPN_P2P_V1
        )

        self.assertIsInstance(request, ConnectionRequestV1)

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

    def test_connection_request_immutable(self):
        """
        Test that we are unable to accidentally mutate fields.
        """
        request = ConnectionRequestV1.parse_file(
            TestData.CONNECTION_FILE_L2VPN_P2P_V1
        )

        self.assertIsInstance(request, ConnectionRequestV1)

        with self.assertRaises(ValidationError):
            request.name = "another-name"

        with self.assertRaises(ValidationError):
            request.description = "another-description"

        with self.assertRaises(ValidationError):
            request.endpoints = []

        # TODO: mutating endpoints do not raise validation error. Why?

        # with self.assertRaises(ValidationError):
        #     request.endpoints[0] = {}

        # with self.assertRaises(ValidationError):
        #     request.endpoints[1] = {}

        with self.assertRaises(ValidationError):
            request.notifications = None

        with self.assertRaises(ValidationError):
            request.notifications[0].email = None

        with self.assertRaises(ValidationError):
            request.scheduling = None

        with self.assertRaises(ValidationError):
            request.scheduling.start_time = None

        with self.assertRaises(ValidationError):
            request.scheduling.end_time = None

        with self.assertRaises(ValidationError):
            request.qos_metrics = None

        with self.assertRaises(ValidationError):
            request.qos_metrics.min_bw = None

        with self.assertRaises(ValidationError):
            request.qos_metrics.min_bw.value = None

        with self.assertRaises(ValidationError):
            request.qos_metrics.min_bw.strict = True

        with self.assertRaises(ValidationError):
            request.qos_metrics.max_delay.value = None

        with self.assertRaises(ValidationError):
            request.qos_metrics.max_delay.strict = None

        with self.assertRaises(ValidationError):
            request.qos_metrics.max_number_oxps = None

        with self.assertRaises(ValidationError):
            request.qos_metrics.max_number_oxps.value = None

        with self.assertRaises(ValidationError):
            request.qos_metrics.max_number_oxps.strict = None

    def test_connection_request_all_vlans_valid(self):
        testdata = {
            "name": "Good connection request for all vlans",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:example.net:p:1",
                    "vlan": "all",
                },
                {
                    "port_id": "urn:sdx:port:example.net:p:2",
                    "vlan": "all",
                },
            ],
        }

        request = ConnectionRequestV1(**testdata)

        self.assertEqual(request.endpoints[0].vlan, "all")
        self.assertEqual(request.endpoints[1].vlan, "all")

    def test_connection_request_all_vlans_valid(self):
        testdata = {
            "name": "Good connection request for all vlans",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:example.net:p:1",
                    "vlan": "1",
                },
                {
                    "port_id": "urn:sdx:port:example.net:p:2",
                    "vlan": "all",
                },
            ],
        }

        self.assertRaisesRegex(
            ValidationError,
            "1 validation error for ConnectionRequestV1",
            ConnectionRequestV1,
            **testdata,
        )

    def test_connection_request_valid_email(self):
        testdata = {
            "name": "Bad connection request: vlan must be in [1,4095] range",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:example.net:p:1",
                    "vlan": "any",
                },
                {
                    "port_id": "urn:sdx:port:example.net:p:2",
                    "vlan": "any",
                },
            ],
            "notifications": [{"email": "alice@example.net"}],
        }

        request = ConnectionRequestV1(**testdata)
        self.assertEqual(request.notifications[0].email, "alice@example.net")

    def test_connection_request_invalid_email(self):
        testdata = {
            "name": "Bad connection request: vlan must be in [1,4095] range",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:example.net:p:1",
                    "vlan": "any",
                },
                {
                    "port_id": "urn:sdx:port:example.net:p:2",
                    "vlan": "any",
                },
            ],
            "notifications": [{"email": "@alice"}],
        }

        self.assertRaisesRegex(
            ValidationError,
            "1 validation error for ConnectionRequestV1",
            ConnectionRequestV1,
            **testdata,
        )


if __name__ == "__main__":
    unittest.main()
