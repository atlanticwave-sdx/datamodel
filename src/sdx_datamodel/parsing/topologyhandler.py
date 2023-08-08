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

            domain_service = data.get("domain_service")
            version = data.get("version")
            time_stamp = data.get("time_stamp")
            nodes = data.get("nodes")
            links = data.get("links")
        except KeyError as e:
            raise MissingAttributeException(data, e.args[0])

        return Topology(
            id=id,
            name=name,
            domain_service=domain_service,
            version=version,
            time_stamp=time_stamp,
            nodes=nodes,
            links=links,
        )

    def import_topology(self, path) -> Topology:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return self.import_topology_data(data)
