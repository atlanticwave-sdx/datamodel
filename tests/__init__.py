from pathlib import Path


class TestData:
    TEST_DATA_DIR = Path(__file__).parent / "data"

    CONNECTION_FILE_P2P = TEST_DATA_DIR / "p2p.json"
    CONNECTION_FILE_REQ = TEST_DATA_DIR / "test_request.json"

    LINK_FILE = TEST_DATA_DIR / "link.json"
    LOCATION_FILE = TEST_DATA_DIR / "location.json"
    NODE_FILE = TEST_DATA_DIR / "node.json"
    PORT_FILE = TEST_DATA_DIR / "port.json"
    SERVICE_FILE = TEST_DATA_DIR / "service.json"

    PORT_FILE_L2VPN_PTP = TEST_DATA_DIR / "port-l2vpn-ptp.json"
    PORT_FILE_L2VPN_PTP_BAD = TEST_DATA_DIR / "port-l2vpn-ptp-bad.json"
    PORT_FILE_L2VPN_PTP_BAD_RANGE = (
        TEST_DATA_DIR / "port-l2vpn-ptp-bad-range.json"
    )

    PORT_FILE_L2VPN_PTP_PTMP = TEST_DATA_DIR / "port-l2vpn-ptp-ptmp.json"
    PORT_FILE_L2VPN_PTP_PTMP_BAD = (
        TEST_DATA_DIR / "port-l2vpn-ptp-ptmp-bad.json"
    )

    TOPOLOGY_AMLIGHT = TEST_DATA_DIR / "amlight.json"
    TOPOLOGY_AMPATH = TEST_DATA_DIR / "ampath.json"
    TOPOLOGY_SAX = TEST_DATA_DIR / "sax.json"
    TOPOLOGY_ZAOXI = TEST_DATA_DIR / "zaoxi.json"
