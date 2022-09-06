import json
from sdxdatamodel.models.connection import Connection
from .exceptions import MissingAttributeException


class ConnectionHandler:
    """
    Parse connection request descritpions.

    Connection request descritpions may be either JSON documents or
    Python dicts.
    """

    def __init__(self):
        """Construct a ConnectionHandler."""
        super().__init__()
        self.connection = None

    def import_connection_data(self, data):
        """
        Create a Connection from connection data encoded in a dict.

        :param data: a dict containing, at a minimum, `id`,
            `name`id(), `ingress_port`, `egress_port` keys.
        """
        try:
            id = data["id"]
            name = data["name"]
            if "bandwidth_required" in data.keys():
                bw = data["bandwidth_required"]
            if "latency_required" in data.keys():
                la = data["latency_required"]
            if "start_time" in data.keys():
                start = data["start_time"]
            if "end_time" in data.keys():
                end = data["end_time"]
            ingress = data["ingress_port"]
            egress = data["egress_port"]
        except KeyError as e:
            raise MissingAttributeException(e.args[0], e.args[0])

        connection = Connection(
            id=id,
            name=name,
            start_time=start,
            end_time=end,
            bandwidth=bw,
            latency=la,
            ingress_port=ingress,
            egress_port=egress,
        )

        return connection

    def import_connection(self, file):
        """
        Import connection descritpion from a file.

        :param file: a JSON document.
        """
        with open(file, "r", encoding="utf-8") as data_file:
            data = json.load(data_file)
            self.connection = self.import_connection_data(data)
        return self.connection

    def get_connection(self):
        """Return connection state."""
        return self.connection
