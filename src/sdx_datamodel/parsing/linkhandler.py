import json

from sdx_datamodel.models.link import Link

from .exceptions import MissingAttributeException


class LinkHandler:
    """
    Handler for parsing the connection request descritpion in JSON.
    """

    def import_link_data(self, data) -> Link:
        try:
            id = data["id"]
            name = data["name"]
            ports = data["ports"]

            short_name = data.get("short_name")

            timestamp = data.get("timestamp")
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
            bandwidth=bandwidth,
            residual_bandwidth=residual_bandwidth,
            latency=latency,
            packet_loss=packet_loss,
            availability=availability,
            private_attributes=private_attributes,
            timestamp=timestamp,
            measurement_period=measurement_period,
        )

    def import_link(self, path) -> Link:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return self.import_link_data(data)
