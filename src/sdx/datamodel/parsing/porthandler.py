import json

from sdx.datamodel.models.port import Port

from .exceptions import MissingAttributeException


class PortHandler:
    """
    Handler for parsing the connection request descritpion in JSON.
    """

    def import_port_data(self, data) -> Port:
        try:
            id = data["id"]
            name = data["name"]

            # node, short_name, label_range, and private_attributes
            # are allowed to be None.
            node = data.get("node")
            short_name = data.get("short_name")
            label_range = data.get("label_range")
            private_attributes = data.get("private_attributes")
        except KeyError as e:
            raise MissingAttributeException(data, e.args[0])

        return Port(
            id=id,
            name=name,
            short_name=short_name,
            node=node,
            label_range=label_range,
            status=None,
            private_attributes=private_attributes,
        )

    def import_port(self, path) -> Port:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return self.import_port_data(data)
