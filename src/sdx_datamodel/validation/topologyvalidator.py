"""
Checks for Topology objects to be in the expected format.
"""

import logging
from re import match

from sdx_datamodel.models.link import Link
from sdx_datamodel.models.location import Location
from sdx_datamodel.models.node import Node
from sdx_datamodel.models.service import Service
from sdx_datamodel.models.topology import SDX_INSTITUTION_ID, Topology

ISO_FORMAT = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[-+]\d{2}:\d{2}"


class TopologyValidator:
    """
    The validation class made to validate a Topology
    """

    def __init__(self, topology: Topology):
        if not isinstance(topology, Topology):
            raise ValueError("TopologyValidator expects a Topology object")

        self._topology = topology
        self._logger = logging.getLogger(__name__)

    def is_valid(self) -> bool:
        errors = self.validate(self._topology, raise_error=False)
        for error in errors:
            self._logger.error(f"{error} in topology '{self._topology.id}'")
        return not bool(errors)

    def validate(self, topology=None, raise_error=True) -> [str]:
        if not topology and self._topology:
            topology = self._topology
        errors = self._validate_topology(topology)
        if errors and raise_error:
            raise ValueError("\n".join(errors))
        return errors

    def _validate_topology(self, topology: Topology):
        """
        Validate that the topology provided meets the JSON schema.

        A topology must have the following:

            - It must meet object standard

            - It must have the default fields: id, name, version,
              timestamp, nodes, and links

            - It must have a Primary owner assigned

            - It must have its primary owner in its institution list

            - It must have the global institution in the institution
              list

        :param topology: The topology being evaluated

        :return: A list of any issues in the data.
        """
        errors = []
        errors += self._validate_object_defaults(topology)

        if SDX_INSTITUTION_ID not in topology.id:
            errors.append(
                f"Global Institution must be in topology {topology.id}"
            )

        service = topology.services
        if service is not None:
            errors += self._validate_service(service, topology)
        for node in topology.nodes:
            errors += self._validate_node(node, topology)
        for link in topology.links:
            errors += self._validate_link(link, topology)

        return errors

    def _validate_service(self, service: Service, topology: Topology):
        """
        Check that institution descritpion meets the XSD standards.

        A institution must have the following:

            - It must meet object default standards.

            - It's Location values are valid

            - The Institution Type must be in the list of valid
              Institution types

        :param institution: The Institution being evaluated.
        :param topology: The Parent Topology.

        :return: A list of any issues in the data.
        """
        errors = []
        errors += self._validate_object_defaults(service)

        return errors

    def _validate_version(self, version, timestamp, topology: Topology):
        """
        Validate that version and timestamp meets ISO standards.

            - It must meet object default standards.

            - It's Location values are valid

            - The Institution Type must be in the list of valid
              Institution types

        :param version: The topology version.
        :param timestamp: The topology time stamp.
        :param topology: The Parent Topology.

        :return: A list of any issues in the data.
        """
        errors = []
        if version:
            if not isinstance(version, str):
                errors.append(f"{topology.id} version must be a string")
            elif not match(ISO_FORMAT, version):
                errors.append(
                    f"{topology.id} version must be datetime ISO format"
                )

        if not match(ISO_FORMAT, timestamp):
            errors.append(
                f"timestamp {timestamp} needs to be in full ISO format"
            )

        return errors

    def _validate_node(self, node: Node, topology: Topology):
        """
        Validate that the node provided meets the XSD standards.

        A node must have the following:

            - It must meet object default standards.

            - It's Location values are valid

        :param node: The Node being evaluated.
        :param topology: The Parent Topology.

        :return: A list of any issues in the data.
        """
        errors = []

        errors += self._validate_object_defaults(node)
        errors += self._validate_location(node.location)

        return errors

    def _validate_link(self, link: Link, topology: Topology):
        """
        Validate that the link provided meets the XSD standards.

        A link must have the following:

            - It must meet object default standards.

            - A link can only connect to 2 nodes

            - The nodes that a link is connected to must be in the
              parent Topology's nodes list

        :param link: The Link being evaluated.
        :param topology: The Parent Topology.

        :return: A list of any issues in the data.
        """
        errors = []
        errors += self._validate_object_defaults(link)

        if len(link._ports) != 2:
            errors.append(
                f"Link {link.id} must connect between 2 ports. "
                f"Currently {link._ports}"
            )
        for port in link._ports:
            if not isinstance(port, (dict, str)):
                errors.append(
                    f"Link {link.id} Port {port} should be "
                    f"a string or a dict. Not {port.__class__.__name__}"
                )
        # TODO: Check ports are in the current topology

        return errors

    def _validate_object_defaults(self, sdx_object):
        """
        Validate that object fields meets XSD standards.

        The object must have the following:

            - The object must have an ID

            - The object ID must be a string

            - The object must have a name

            - The object name must be a string

            - If the object has a short name, it must be a string

            - If the object has a version, it must be a string in ISO
              format

            - All the additional properties on the object are proper

        :param sdx_object: The sdx Model Object being evaluated.

        :return: A list of any issues in the data.
        """
        errors = []
        if not sdx_object._id:
            errors.append(f"{sdx_object.__class__.__name__} must have an ID")
        if not isinstance(sdx_object._id, str):
            errors.append(
                f"{sdx_object.__class__.__name__} ID must be a string"
            )
        if not sdx_object._name:
            errors.append(
                f"{sdx_object.__class__.__name__} {sdx_object._name} must have a name"
            )
        if not isinstance(sdx_object._name, str):
            errors.append(
                f"{sdx_object.__class__.__name__} {sdx_object._name} name must be a string"
            )

        return errors

    def _validate_location(self, location: Location, enforce_coordinates=True):
        """
        Validate that the object location fields meets the XSD
        standards.  The location must have the following:

            - A location must have a longitude

            - A location's longitude muse be a floating point value

            - A location's longitude must be between -180 and -180

            - A location must have a latitude

            - A location must be a floating point value

            - A location's latitude must be between -90 and 90

            - A location's altitude must be a floating point value

            - A location's UN/LOCODE must be a string value

            - A location's address must be a string or a list of
              strings

        :param location: The Location Object being evaluated.
        :param enforce_coordinates: A boolean determining if longitude
            and latitude should be enforced

        :return: A list of any issues in the data.
        """
        errors = []
        if location.longitude is None and enforce_coordinates:
            errors.append(
                f"{location.__class__.__name__} "
                f"Longitude must be set to a value"
            )
        try:
            if location.longitude is not None:
                if not -180 <= float(location.longitude) <= 180:
                    errors.append(
                        f"{location.__class__.__name__} "
                        f"Longitude must be a value that is between -180 and 180"
                    )
        except ValueError:
            errors.append(
                f"{location.__class__.__name__} "
                f"Longitude must be a floating point value"
            )

        if location.latitude is None and enforce_coordinates:
            errors.append(
                f"{location.__class__.__name__} "
                f"Latitude must be set to a value"
            )
        try:
            if location.latitude is not None:
                if not -90 <= float(location.latitude) <= 90:
                    errors.append(
                        f"{location.__class__.__name__} "
                        f"Latitude must be a value that is between -90 and 90"
                    )
        except ValueError:
            errors.append(
                f"{location.__class__.__name__} "
                f"Latitude must be a floating point value"
            )

        try:
            if location.latitude:
                float(location.latitude)
        except ValueError:
            errors.append(
                f"{location.__class__.__name__} "
                f"Latitude must be a floating point value"
            )

        if not location.address:
            errors.append(
                f"{location.__class__.__name__} " f"Address must exist"
            )
        if not type(location.address) == str:
            errors.append(
                f"{location.__class__.__name__} {location} "
                f"Address {location.address} must be a string"
            )

        if not location.iso3166_2_lvl4:
            errors.append(
                f"{location.__class__.__name__} {location} "
                f"ISO3166-2-Lvl4 must exist"
            )
        if not type(location.iso3166_2_lvl4) == str:
            errors.append(
                f"{location.__class__.__name__} {location} "
                f"ISO3166-2-Lvl4 {location.iso3166_2_lvl4} must be a string"
            )

        return errors
