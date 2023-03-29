import pathlib


class TestData:
    TEST_DATA_DIR = pathlib.Path(__file__).parent.joinpath("data")

    CONNECTION_FILE_P2P = TEST_DATA_DIR.joinpath("p2p.json")
    CONNECTION_FILE_REQ = TEST_DATA_DIR.joinpath("test_request.json")

    LINK_FILE = TEST_DATA_DIR.joinpath("link.json")
    LOCATION_FILE = TEST_DATA_DIR.joinpath("location.json")
    NODE_FILE = TEST_DATA_DIR.joinpath("node.json")
    PORT_FILE = TEST_DATA_DIR.joinpath("port.json")
    SERVICE_FILE = TEST_DATA_DIR.joinpath("service.json")

    TOPOLOGY_AMLIGHT = TEST_DATA_DIR.joinpath("amlight.json")
    TOPOLOGY_AMPATH = TEST_DATA_DIR.joinpath("ampath.json")
    TOPOLOGY_SAX = TEST_DATA_DIR.joinpath("sax.json")
    TOPOLOGY_ZAOXI = TEST_DATA_DIR.joinpath("zaoxi.json")
