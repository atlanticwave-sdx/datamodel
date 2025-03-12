import json

from sdx_datamodel.models.topology import Topology
from sdx_datamodel.parsing.exceptions import MissingAttributeException


class TopologyHandler:
    """
    Handler for parsing topology descritpion data.
    """

    def import_topology_data(self, data) -> Topology:
        try:
            id = data["id"]
            name = data["name"]

            # optional fields
            model_version = data.get("model_version")
            domain_service = data.get("services")
            version = data.get("version")
            timestamp = data.get("timestamp")
            nodes = data.get("nodes")
            links = data.get("links")
        except KeyError as e:
            raise MissingAttributeException(data, e.args[0])

        return Topology(
            id=id,
            name=name,
            model_version=model_version,
            services=domain_service,
            version=version,
            timestamp=timestamp,
            nodes=nodes,
            links=links,
        )

    def import_topology(self, path) -> Topology:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return self.import_topology_data(data)
