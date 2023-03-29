import json

from sdx.datamodel.models.node import Node

from .exceptions import MissingAttributeException


class NodeHandler:

    """
    Handler for parsing node data.
    """

    def __init__(self):
        super().__init__()

    def import_node_data(self, data) -> Node:
        try:
            id = data["id"]
            name = data["name"]
            short_name = data["short_name"]
            location = data["location"]
            ports = data["ports"]

            # private_attributes is optional.
            private_attributes = data.get("private_attributes")
        except KeyError as e:
            raise MissingAttributeException(data, e.args[0])

        return Node(
            id=id,
            name=name,
            short_name=short_name,
            location=location,
            ports=ports,
            private_attributes=private_attributes,
        )

    def import_node(self, path) -> Node:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return self.import_node_data(data)
