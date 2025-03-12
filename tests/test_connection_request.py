import datetime
import json
import unittest

from pydantic import ValidationError

from sdx_datamodel.models.connection_request import (
    ConnectionRequestV0,
    ConnectionRequestV1,
)

from . import TestData


class TestConnectionRequestV1(unittest.TestCase):
    """
    Tests for ConnectionRequestV1.
    """

    def test_connection_request_basic(self):
        """
        Test a basic connection request.
        """
        testdata = json.loads(
            TestData.CONNECTION_FILE_L2VPN_VLAN_TRANS_V1.read_text()
        )
        request = ConnectionRequestV1(**testdata)

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

    def test_connection_request_amlight_zaoxi(self):
        """
        Validate the example request.
        """
        testdata = json.loads(
            TestData.CONNECTION_FILE_L2VPN_AMLIGHT_ZAOXI_V1.read_text()
        )
        request = ConnectionRequestV1(**testdata)

        self.assertIsInstance(request, ConnectionRequestV1)

        self.assertEqual(request.name, "new-connection")
        self.assertEqual(request.description, "a test circuit")

        self.assertEqual(len(request.endpoints), 2)

        self.assertEqual(
            request.endpoints[0].port_id,
            "urn:sdx:port:amlight.net:A1:3",
        )
        self.assertEqual(request.endpoints[0].vlan, "101")

        self.assertEqual(
            request.endpoints[1].port_id, "urn:sdx:port:zaoxi:B2:1"
        )
        self.assertEqual(request.endpoints[1].vlan, "101")

    def test_connection_request_empty(self):
        """
        Empty requests are invalid.
        """
        testdata = {}

        self.assertRaisesRegex(
            ValidationError,
            "2 validation errors for ConnectionRequestV1",
            ConnectionRequestV1,
            **testdata,
        )

    def test_connection_request_no_endpoints(self):
        """
        Requests that contain no endpoints are invalid.
        """
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
        """
        Requests that have empty endpoints are invalid.
        """
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
        """
        Requests that contain only one endpoint are invalid.
        """
        testdata = {
            "name": "no-endpoints",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:example.net:p:1",
                    "vlan": "100",
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
        """
        VLANs are required to be strings.
        """
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
        """
        VLANs are required to be in the [1,4095] range.
        """
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
        """
        Ranges are required to be valid numbers.
        """
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
        """
        Numbers in ranges are required to be within [1,4095] range.
        """
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
        """
        Ranges should be in numbers, and numbers in ranges are
        required to be within [1,4095] range.
        """
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
        """
        VLANs in both endpoints can be `all`.
        """
        testdata = {
            "name": "Good connection request: both VLANs are `all`",
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
        """
        VLANs in both endpoints can be `any`.
        """
        testdata = {
            "name": "Good connection request: both VLANs are `any`",
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
        """
        VLANs are required to be numbers, ranges, or certain strings
        such as "all", "any", or "untagged".
        """
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
        """
        When one endpoint has the VLAN range option in use, all other
        endpoint(s) must have the same VLAN range.
        """
        request_name = "Connection request with valid vlan ranges"
        port0_id = "urn:sdx:port:example.net:p:1"
        vlan_range = "100:200"
        port1_id = "urn:sdx:port:example.net:p:2"
        testdata = {
            "name": request_name,
            "endpoints": [
                {
                    "port_id": port0_id,
                    "vlan": vlan_range,
                },
                {
                    "port_id": port1_id,
                    "vlan": vlan_range,
                },
            ],
        }

        request = ConnectionRequestV1(**testdata)
        self.assertEqual(request.name, request_name)
        self.assertEqual(request.endpoints[0].port_id, port0_id)
        self.assertEqual(request.endpoints[0].vlan, vlan_range)
        self.assertEqual(request.endpoints[1].port_id, port1_id)
        self.assertEqual(request.endpoints[1].vlan, vlan_range)

    def test_connection_request_vlan_invalid_unmatched_range(self):
        """
        When one endpoint has the VLAN range option in use, all other
        endpoint(s) must have the same VLAN range.
        """
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

        self.assertRaisesRegex(
            ValidationError,
            "1 validation error for ConnectionRequestV1",
            ConnectionRequestV1,
            **testdata,
        )

    def test_connection_request_vlan_inverse_invalid_range(self):
        """
        Ranges like n1:n2 where n2 < n1 are invalid.
        """
        request_name = "Connection request with valid vlan ranges"
        port0_id = "urn:sdx:port:example.net:p:1"
        vlan_range = "200:100"
        port1_id = "urn:sdx:port:example.net:p:2"
        testdata = {
            "name": request_name,
            "endpoints": [
                {
                    "port_id": port0_id,
                    "vlan": vlan_range,
                },
                {
                    "port_id": port1_id,
                    "vlan": vlan_range,
                },
            ],
        }

        self.assertRaisesRegex(
            ValidationError,
            "2 validation errors for ConnectionRequestV1",
            ConnectionRequestV1,
            **testdata,
        )

    def test_connection_request_with_optional_fields(self):
        """
        Test a connection request that has optional fields.
        """
        testdata = json.loads(
            TestData.CONNECTION_FILE_L2VPN_P2P_V1.read_text()
        )
        request = ConnectionRequestV1(**testdata)

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

        # TODO: `TzInfo` is a type internal to Pydantic. I don't know
        # how to compare a thing containing `TzInfo`.

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

        testdata = json.loads(
            TestData.CONNECTION_FILE_L2VPN_P2P_V1.read_text()
        )
        request = ConnectionRequestV1(**testdata)

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
        """
        If one VLAN in a request is "all", all VLANs should be "all".
        """
        testdata = {
            "name": "Bad connection request with 'all' in vlans",
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
        """
        Requests containing valid notification emails.
        """
        testdata = {
            "name": "Connection request with valid email in notifications",
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
            "notifications": [
                {"email": "alice@example.net"},
                {"email": "bob@example.org"},
            ],
        }

        request = ConnectionRequestV1(**testdata)
        self.assertEqual(request.notifications[0].email, "alice@example.net")
        self.assertEqual(request.notifications[1].email, "bob@example.org")

    def test_connection_request_invalid_email(self):
        """
        Requests containing invalid notification emails.
        """
        testdata = {
            "name": "Connection request with invalid email in notifications",
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


class TestConnectionRequestV0(unittest.TestCase):
    """
    Tests for ConnectionRequestV0.
    """

    def test_connection_request_v0_basic(self):
        """
        Basic checks for a basic V0 connection request.
        """

        testdata = json.loads(TestData.CONNECTION_FILE_REQ.read_text())
        request = ConnectionRequestV0(**testdata)

        self.assertIsInstance(request, ConnectionRequestV0)

        self.assertEqual(request.id, "285eea4b-1e86-4d54-bd75-f14b8cb4a63a")
        self.assertEqual(request.name, "Test connection request")

        self.assertEqual(request.bandwidth_required, 10)
        self.assertEqual(request.latency_required, 300)

        # No start/end times in this request.
        self.assertIsNone(request.start_time)
        self.assertIsNone(request.end_time)

        self.assertEqual(request.ingress_port.id, "urn:sdx:port:zaoxi:A1:2")
        self.assertEqual(request.ingress_port.name, "Novi100:2")
        self.assertEqual(
            request.ingress_port.node, "urn:ogf:network:sdx:node:zaoxi:A1"
        )
        self.assertEqual(request.ingress_port.status, "up")

        self.assertEqual(
            request.egress_port.id, "urn:sdx:port:amlight.net:A1:1"
        )
        self.assertEqual(request.egress_port.name, "Novi100:1")
        self.assertEqual(
            request.egress_port.node, "urn:sdx:node:amlight.net:A1"
        )
        self.assertEqual(request.egress_port.status, "up")

    def test_connection_request_v0_no_node(self):
        """
        Check a V0 connection request that does not carry the optional
        fields.
        """

        testdata = json.loads(TestData.CONNECTION_FILE_REQ_NO_NODE.read_text())
        request = ConnectionRequestV0(**testdata)

        self.assertIsInstance(request, ConnectionRequestV0)

        self.assertIsNone(request.ingress_port.node)
        self.assertIsNone(request.ingress_port.status)

        self.assertIsNone(request.egress_port.node)
        self.assertIsNone(request.egress_port.status)

    def test_connection_request_v0_p2p(self):
        """
        Check the P2P request in v0 format.
        """
        testdata = json.loads(TestData.CONNECTION_FILE_P2P.read_text())
        request = ConnectionRequestV0(**testdata)

        self.assertIsInstance(request, ConnectionRequestV0)

        self.assertIsNotNone(request.ingress_port.id)
        self.assertIsNotNone(request.ingress_port.name)
        self.assertIsNotNone(request.ingress_port.short_name)
        self.assertIsNotNone(request.ingress_port.label)
        self.assertIsNotNone(request.ingress_port.label_range)
        self.assertIsNotNone(request.ingress_port.node)
        self.assertIsNone(request.ingress_port.status)

        self.assertIsNotNone(request.egress_port.id)
        self.assertIsNotNone(request.egress_port.name)
        self.assertIsNotNone(request.egress_port.short_name)
        self.assertIsNotNone(request.egress_port.label)
        self.assertIsNotNone(request.egress_port.label_range)
        self.assertIsNotNone(request.egress_port.node)
        self.assertIsNone(request.egress_port.status)


if __name__ == "__main__":
    unittest.main()
