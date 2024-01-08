import json
import logging
import pathlib
from os import PathLike
from typing import List, Union

from sdx_datamodel.models.port import Port
from sdx_datamodel.parsing.exceptions import (
    InvalidVlanRangeException,
    MissingAttributeException,
)


class PortHandler:
    """
    Handler for parsing the connection request descritpion in JSON.
    """

    def __init__(self):
        self._logger = logging.getLogger(__name__)

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
            #
            # TODO: actually use the services value.  We might want to
            # pass it on to Port instance we create, so Port instance
            # may need a services field.  Port class is generated from
            # SDX-LC's OpenAPI spec, so the spec will have to be
            # updated.
            services = self._validate_l2vpn_services(
                services=data.get("services"), port_id=id
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

    def _validate_l2vpn_services(self, services: Union[dict, None], port_id):
        """
        Validate any "service" attached to a port definition.

        This method is intended to cover L2VPN services specified in
        SDX Topology Data Model spec 2.0.0.

        https://docs.google.com/document/d/1lgxjIT144EFu1G_OVcU19hN1cSUT_v2-tE0Z-7UlkNg/view#

        There's an existing "domain service" also (see models.Service
        and SDX-LC OpenAPI spec), which seems to conflict with L2VPN
        service.
        """
        if not services:
            self._logger.warning(f"No services defined in port '{port_id}'")
            return None

        if not isinstance(services, dict):
            self._logger.warning(
                f"Service {services} is not a dict in {port_id}"
            )
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

        self._logger.info(
            f"Found l2vpn_ptp_vlan_range: {l2vpn_ptp_vlan_range}, "
            f"l2vpn_ptmp_vlan_range: {l2vpn_ptmp_vlan_range} "
            f"in port '{port_id}'"
        )

        # TODO: Perhaps return a Service, or maybe a L2VPN Service?
        # The models.Service class seems to refer to domain services
        # specifically, and it is possibly generated from SDX-LC's
        # OpenAPI spec.  We need to find a way to clear up things.
        return l2vpn_ptp_vlan_range, l2vpn_ptmp_vlan_range

    def _validate_vlan_range(self, vlan_range: list) -> List[List[int]]:
        """
        Parse VLAN ranges.

        VLAN range is of the format [[1, 100], [300, 305], 200], ie.,
        it is a list whose elements are either numbers or number
        pairs.  Raise an exception when they are not of that form.
        """
        if not vlan_range or not isinstance(vlan_range, list):
            raise InvalidVlanRangeException(
                f"VLAN range ({vlan_range}) must be a list, but is {type(vlan_range)}"
            )

        for item in vlan_range:
            if not isinstance(item, list):
                if not isinstance(item, int):
                    raise InvalidVlanRangeException(
                        f"VLAN range must be a list or a number, but {item} is not"
                    )

            if isinstance(item, list):
                if len(item) != 2:
                    raise InvalidVlanRangeException(
                        f"VLAN range {item} is not a list of 2 numbers"
                    )

                if not all(isinstance(vlan, int) for vlan in item):
                    raise InvalidVlanRangeException(
                        f"VLAN ranges in {item} must be numbers, but it is not"
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
        data = json.loads(pathlib.Path(path).read_text())
        return self.import_port_data(data)
