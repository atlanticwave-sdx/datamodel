import json

from sdx.datamodel.models.port import Port

from .exceptions import MissingAttributeException


class PortHandler:
    """
    Handler for parsing the connection request descritpion in JSON.
    """

    def __init__(self):
        super().__init__()
        self.port = None

    def import_port_data(self, data) -> Port:
        try:
            id = data["id"]
            name = data["name"]

            # node, short_name, l_r, and p_a are allowed to be None.
            node = data.get("node", None)
            short_name = data.get("short_name", None)
            l_r = data.get("label_range", None)
            p_a = data.get("private_attributes", None)
        except KeyError as e:
            raise MissingAttributeException(data, e.args[0])

        self.port = Port(
            id=id,
            name=name,
            short_name=short_name,
            node=node,
            label_range=l_r,
            status=None,
            private_attributes=p_a,
        )

        return self.port

    def import_port(self, file) -> Port:
        with open(file, "r", encoding="utf-8") as data_file:
            data = json.load(data_file)
            self.port = self.import_port_data(data)
        return self.port

    def get_port(self) -> Port:
        return self.port
