import json
from os import PathLike
from typing import List, Union

from sdx.datamodel.models.port import Port
from sdx.datamodel.parsing.exceptions import (
    InvalidVlanRangeException,
    MissingAttributeException,
)


class PortHandler:
    """
    Handler for parsing the connection request descritpion in JSON.
    """

    def import_port_data(self, data: dict) -> Port:
        try:
            id = data["id"]
            name = data["name"]

            # node, short_name, label_range, and private_attributes
            # are allowed to be None.
            node = data.get("node")
            short_name = data.get("short_name")
            label_range = data.get("label_range")
            private_attributes = data.get("private_attributes")

            # L2VPN services are optional.
            # TODO: actually use services value.
            services = self._validate_l2vpn_services(
                services=data.get("services")
            )

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

    def _validate_l2vpn_services(self, services: Union[dict, None]):
        if not services:
            print("No services defined")
            return None

        if not isinstance(services, dict):
            print(f"Service {services} is not a dict")
            return None

        if services and services.get("l2vpn-ptp"):
            vlan_range = services.get("l2vpn-ptp").get("vlan_range")
            l2vpn_ptp_vlan_range = self._validate_vlan_range(vlan_range)
        else:
            l2vpn_ptp_vlan_range = None

        if isinstance(services, dict) and services.get("l2vpn-ptmp"):
            vlan_range = services.get("l2vpn-ptmp").get("vlan_range")
            l2vpn_ptmp_vlan_range = self._validate_vlan_range(vlan_range)
        else:
            l2vpn_ptmp_vlan_range = None

        print(f"l2vpn_ptp_vlan_range: {l2vpn_ptp_vlan_range}")
        print(f"l2vpn_ptmp_vlan_range: {l2vpn_ptmp_vlan_range}")

        # TODO: Perhaps return a Service, or maybe a L2VPN Service?
        # The models.Service class seems to refer to domain services
        # specifically, and it is possibly generated from SDX-LC's
        # OpenAPI spec.  We need to find a way to clear up things.
        return l2vpn_ptp_vlan_range, l2vpn_ptmp_vlan_range

    def _validate_vlan_range(self, vlan_range: list) -> List[List[int]]:
        """
        Parse VLAN ranges.

        VLAN range is of the format [[1, 100], [300, 305]].  Raise an
        exception when they are not of that form.
        """
        if not vlan_range or not isinstance(vlan_range, list):
            raise InvalidVlanRangeException(
                f"VLAN range ({vlan_range}) must be a list, but is {type(vlan_range)}"
            )

        for item in vlan_range:
            if not isinstance(item, list) and len(item) != 2:
                raise InvalidVlanRangeException(
                    f"VLAN range item must be a list of length 2, but is {item}"
                )

            if not isinstance(item[0], int) or not isinstance(item[1], int):
                raise InvalidVlanRangeException(
                    f"VLAN range in {item} must be numbers, but it is not"
                )

            if item[0] >= item[1]:
                raise InvalidVlanRangeException(
                    f"VLAN range {item} is invalid: {item[0]} >= {item[1]}"
                )

        return vlan_range

    def import_port(
        self, path: Union[str, bytes, PathLike]
    ) -> Union[Port, None]:
        """
        Import port data from a JSON file.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return self.import_port_data(data)
        except Exception as e:
            print(f"Error decoding JSON: {e}")
            return None
