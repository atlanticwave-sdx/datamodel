import json

from sdx.datamodel.models.link import Link

from .exceptions import MissingAttributeException


class LinkHandler:

    """
    Handler for parsing the connection request descritpion in JSON.
    """

    def __init__(self):
        super().__init__()

    def import_link_data(self, data) -> Link:
        try:
            id = data["id"]
            name = data["name"]
            ports = data["ports"]

            short_name = data.get("short_name")
            nni = bool(data.get("nni"))
            timestamp = data.get("time_stamp")
            bandwidth = data.get("bandwidth")
            residual_bandwidth = data.get("residual_bandwidth")
            latency = data.get("latency")
            packet_loss = data.get("packet_loss")
            private_attributes = data.get("private_attributes")
            availability = data.get("availability")
            measurement_period = data.get("measurement_period")
        except KeyError as e:
            raise MissingAttributeException(data, e.args[0])

        return Link(
            id=id,
            name=name,
            short_name=short_name,
            ports=ports,
            nni=nni,
            bandwidth=bandwidth,
            residual_bandwidth=residual_bandwidth,
            latency=latency,
            packet_loss=packet_loss,
            availability=availability,
            private_attributes=private_attributes,
            time_stamp=timestamp,
            measurement_period=measurement_period,
        )

    def import_link(self, path) -> Link:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return self.import_link_data(data)
