import json
import unittest
from pathlib import Path

import jsonschema

from . import TestData


class JSONSchemaTests(unittest.TestCase):
    """
    Test data files against corresponding JSON schema.
    """

    SCHEMA_DIR = Path(__file__).parent.parent / "schemas"

    CONNECTION_SCHEMA_FILE = SCHEMA_DIR / "Connection.json"
    LINK_SCHEMA_FILE = SCHEMA_DIR / "Link.json"
    LOCATION_SCHEMA_FILE = SCHEMA_DIR / "Location.json"
    NODE_SCHEMA_FILE = SCHEMA_DIR / "Node.json"
    PATH_SCHEMA_FILE = SCHEMA_DIR / "Path.json"
    PORT_SCHEMA_FILE = SCHEMA_DIR / "Port.json"
    SERVICE_SCHEMA_FILE = SCHEMA_DIR / "Service.json"
    TOPOLOGY_SCHEMA_FILE = SCHEMA_DIR / "Topology.json"

    def _read_json(self, path: Path):
        """
        Read JSON and return a dict.
        """
        return json.loads(path.read_text())

    def test_connection_request_schema(self):
        jsonschema.validate(
            self._read_json(TestData.CONNECTION_FILE_REQ),
            self._read_json(self.CONNECTION_SCHEMA_FILE),
        )

    def test_link_schema(self):
        jsonschema.validate(
            self._read_json(TestData.LINK_FILE),
            self._read_json(self.LINK_SCHEMA_FILE),
        )

    def test_location_schema(self):
        jsonschema.validate(
            self._read_json(TestData.LOCATION_FILE),
            self._read_json(self.LOCATION_SCHEMA_FILE),
        )

    def test_node_schema(self):
        jsonschema.validate(
            self._read_json(TestData.NODE_FILE),
            self._read_json(self.NODE_SCHEMA_FILE),
        )

    @unittest.skip(reason="Path files are not implemented.")
    def test_path_schema(self):
        jsonschema.validate(
            self._read_json(TestData.PATH_FILE),
            self._read_json(self.PATH_SCHEMA_FILE),
        )

    def test_port_schema(self):
        jsonschema.validate(
            self._read_json(TestData.PORT_FILE),
            self._read_json(self.PORT_SCHEMA_FILE),
        )

    def test_service_schema(self):
        jsonschema.validate(
            self._read_json(TestData.SERVICE_FILE),
            self._read_json(self.SERVICE_SCHEMA_FILE),
        )

    def test_topology_schema(self):
        jsonschema.validate(
            self._read_json(TestData.TOPOLOGY_FILE_AMLIGHT),
            self._read_json(self.TOPOLOGY_SCHEMA_FILE),
        )


if __name__ == "__main__":
    unittest.main()
