from pathlib import Path

try:
    # Use stdlib modules with Python > 3.8.
    from importlib.resources import files
except:
    # Use compatibility library with Python 3.8.
    from importlib_resources import files


class TestData:
    # Some data files are in src/sdx_datamodel/data.
    PACKAGE_DATA_DIR = files("sdx_datamodel") / "data"

    TOPOLOGY_DIR = PACKAGE_DATA_DIR / "topologies"
    TOPOLOGY_FILE_ZAOXI = TOPOLOGY_DIR / "zaoxi.json"
    TOPOLOGY_FILE_SAX = TOPOLOGY_DIR / "sax.json"
    TOPOLOGY_FILE_AMLIGHT = TOPOLOGY_DIR / "amlight.json"

    REQUESTS_DIR = PACKAGE_DATA_DIR / "requests"
    CONNECTION_FILE_REQ = REQUESTS_DIR / "test_request.json"
    CONNECTION_FILE_REQ_NO_NODE = REQUESTS_DIR / "test_request_no_node.json"
    CONNECTION_FILE_P2P = REQUESTS_DIR / "p2p.json"

    # The Remaining test data files are in tests/data.
    TEST_DATA_DIR = Path(__file__).parent / "data"

    LINK_FILE = TEST_DATA_DIR / "link.json"
    LOCATION_FILE = TEST_DATA_DIR / "location.json"
    NODE_FILE = TEST_DATA_DIR / "node.json"
    PORT_FILE = TEST_DATA_DIR / "port.json"
    SERVICE_FILE = TEST_DATA_DIR / "service.json"

    PORT_FILE_L2VPN_PTP = TEST_DATA_DIR / "port-l2vpn-ptp.json"
    PORT_FILE_L2VPN_PTP_INVALID = TEST_DATA_DIR / "port-l2vpn-ptp-invalid.json"
    PORT_FILE_L2VPN_PTP_BAD_RANGE = (
        TEST_DATA_DIR / "port-l2vpn-ptp-bad-range.json"
    )

    PORT_FILE_L2VPN_PTP_PTMP = TEST_DATA_DIR / "port-l2vpn-ptp-ptmp.json"
    PORT_FILE_L2VPN_PTP_PTMP_INVALID = (
        TEST_DATA_DIR / "port-l2vpn-ptp-ptmp-invalid.json"
    )

    TOPOLOGY_AMPATH = TEST_DATA_DIR / "ampath.json"
