import pathlib
import unittest

from sdx.datamodel.models.node import Node
from sdx.datamodel.parsing.exceptions import MissingAttributeException
from sdx.datamodel.parsing.nodehandler import NodeHandler


class TestNodeHandler(unittest.TestCase):
    TEST_DATA_DIR = pathlib.Path(__file__).parent.joinpath("data")
    NODE_FILE = TEST_DATA_DIR.joinpath("node.json")

    def test_import_node(self):
        node = NodeHandler().import_node(self.NODE_FILE)
        print(f"Node: {node}")
        self.assertIsInstance(node, Node)

    def test_import_empty_node(self):
        self.assertRaisesRegex(
            MissingAttributeException,
            "Missing required attribute 'id' while parsing <{}>",
            NodeHandler().import_node_data,
            {},
        )

    def test_import_null_node(self):
        self.assertRaisesRegex(
            TypeError,
            "expected str, bytes or os.PathLike object, not NoneType",
            NodeHandler().import_node,
            None,
        )


if __name__ == "__main__":
    unittest.main()
