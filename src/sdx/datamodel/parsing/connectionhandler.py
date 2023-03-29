import json

from sdx.datamodel.models.connection import Connection
from sdx.datamodel.models.port import Port
from sdx.datamodel.parsing.porthandler import PortHandler

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

    def import_connection_data(self, data: dict) -> Connection:
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
            ingress_port = self._make_port(data, "ingress_port")
            egress_port = self._make_port(data, "egress_port")

            # bandwidth_required, latency_required, start_time, and
            # end_time are optional, and can be None.
            bandwidth_required = data.get("bandwidth_required")
            latency_required = data.get("latency_required")
            start_time = data.get("start_time")
            end_time = data.get("end_time")
        except KeyError as e:
            raise MissingAttributeException(data, e.args[0])

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

    def import_connection(self, path) -> Connection:
        """
        Import connection descritpion from a file.

        :param path: Path to a JSON document.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return self.import_connection_data(data)

    def _make_port(self, connection_data: dict, port_name: str) -> Port:
        """
        Construct a Port object from the given descritpion.

        :param connection_data: a dict that describes a connection.
        :param port_name: "ingress_port" or "egress_port"
        :return: a Port object.
        """
        port_data = connection_data.get(port_name)

        if port_data is None:
            raise MissingAttributeException(connection_data, port_name)

        port_handler = PortHandler()
        return port_handler.import_port_data(port_data)
