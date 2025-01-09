import json

from sdx_datamodel.models.connection import Connection
from sdx_datamodel.models.port import Port
from sdx_datamodel.parsing.porthandler import PortHandler

from .exceptions import MissingAttributeException


class ConnectionHandler:
    """
    Parse connection request descritpions.

    Connection request descritpions may be either JSON documents or
    Python dicts.
    """

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
            bandwidth_required = None
            latency_required = None
            if data.get("endpoints") is not None:  # spec version 2.0.0
                endpoints = data.get("endpoints")
                if len(endpoints) != 2:
                    raise ValueError("endpoints must have 2 elements")
                ingress_port = self._make_port(endpoints[0], "")
                egress_port = self._make_port(endpoints[1], "")

                qos_metrics = data.get("qos_metrics", {})
                bandwidth_required_obj = qos_metrics.get("min_bw")
                if bandwidth_required_obj is not None:
                    bandwidth_required = bandwidth_required_obj.get("value")
                latency_required_obj = qos_metrics.get("max_delay")
                if latency_required_obj is not None:
                    latency_required = latency_required_obj.get("value")

                scheduling = data.get("scheduling", {})
                start_time = scheduling.get("start_time")
                end_time = scheduling.get("end_time")

            else:  # spec version 1.0.0
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
            bandwidth_required=bandwidth_required,
            latency_required=latency_required,
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
        if port_name == "":
            port_data = connection_data
        else:
            port_data = connection_data.get(port_name)

        if port_data is None:
            raise MissingAttributeException(connection_data, port_name)

        if port_data.get("port_id") is not None:
            port_data["id"] = port_data["port_id"]
            port_data["name"] = port_data["port_id"]
            del port_data["port_id"]

        vlan = port_data.get("vlan")
        if vlan is not None:
            port_data["vlan_range"] = int(vlan) if vlan.isdigit() else vlan
            del port_data["vlan"]

        port_handler = PortHandler()
        return port_handler.import_port_data(port_data)
