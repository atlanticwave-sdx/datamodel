import json

from sdxdatamodel.models.connection import Connection
from sdxdatamodel.models.port import Port
from sdxdatamodel.parsing.porthandler import PortHandler

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
            # The fields id, name, ingress_port, and egress_port are
            # required, and failure to find them in the dict must throw
            # a KeyError.
            id = data["id"]
            name = data["name"]

            # Construct ports here.
            ingress_port = self._make_port(data["ingress_port"])
            egress_port = self._make_port(data["egress_port"])

            # bandwidth_required, latency_required, start_time, and
            # end_time are optional, and can be None.
            bandwidth_required = data.get("bandwidth_required", None)
            latency_required = data.get("latency_required", None)
            start_time = data.get("start_time", None)
            end_time = data.get("end_time", None)
        except KeyError as e:
            raise MissingAttributeException(e.args[0], e.args[0])

        return Connection(
            id=id,
            name=name,
            start_time=start_time,
            end_time=end_time,
            bandwidth=bandwidth_required,
            latency=latency_required,
            ingress_port=ingress_port,
            egress_port=egress_port,
        )

    def _make_port(self, port_data: dict) -> Port:
        """
        Construct a Port object from the given descritpion.
        """
        if port_data is None:
            # Not a very good error here; making do.
            raise MissingAttributeException(
                "egress_port/ingress_port", port_data
            )

        port_handler = PortHandler()
        return port_handler.import_port_data(port_data)

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
