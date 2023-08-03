import unittest

from sdx_datamodel.models.node import Node
from sdx_datamodel.parsing.exceptions import MissingAttributeException
from sdx_datamodel.parsing.nodehandler import NodeHandler

from . import TestData


class NodeHandlerTests(unittest.TestCase):
    def test_import_node(self):
        node = NodeHandler().import_node(TestData.NODE_FILE)
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
