# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from sdx_datamodel import util
from sdx_datamodel.models.base_model_ import Model
from sdx_datamodel.models.location import Location  # noqa: F401,E501
from sdx_datamodel.models.port import Port  # noqa: F401,E501
from sdx_datamodel.parsing.locationhandler import LocationHandler
from sdx_datamodel.parsing.porthandler import PortHandler


class Node(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(
        self,
        id=None,
        name=None,
        short_name=None,
        location=None,
        ports=None,
        private_attributes=None,
    ):  # noqa: E501
        """Node - a model defined in Swagger

        :param id: The id of this Node.  # noqa: E501
        :type id: str
        :param name: The name of this Node.  # noqa: E501
        :type name: str
        :param short_name: The short_name of this Node.  # noqa: E501
        :type short_name: str
        :param location: The location of this Node.  # noqa: E501
        :type location: Location
        :param ports: The ports of this Node.  # noqa: E501
        :type ports: List[Port]
        :param private_attributes: The private_attributes of this Node.  # noqa: E501
        :type private_attributes: List[str]
        """
        self.swagger_types = {
            "id": str,
            "name": str,
            "short_name": str,
            "location": Location,
            "ports": List[Port],
            "private_attributes": List[str],
        }

        self.attribute_map = {
            "id": "id",
            "name": "name",
            "short_name": "short_name",
            "location": "location",
            "ports": "ports",
            "private_attributes": "private_attributes",
        }
        self._id = id
        self._name = name
        if short_name is not None:
            self._short_name = short_name
        self._location = None
        self._location = self.set_location(location)
        self._ports = []
        self._ports = self.set_ports(ports)
        if private_attributes is not None:
            self._private_attributes = private_attributes

    @classmethod
    def from_dict(cls, dikt):
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The node of this Node.  # noqa: E501
        :rtype: Node
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Node.


        :return: The id of this Node.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Node.


        :param id: The id of this Node.
        :type id: str
        """
        if id is None:
            raise ValueError(
                "Invalid value for `id`, must not be `None`"
            )  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this Node.


        :return: The name of this Node.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Node.


        :param name: The name of this Node.
        :type name: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501

        self._name = name

    @property
    def short_name(self):
        """Gets the short_name of this Node.


        :return: The short_name of this Node.
        :rtype: str
        """
        return self._short_name

    @short_name.setter
    def short_name(self, short_name):
        """Sets the short_name of this Node.


        :param short_name: The short_name of this Node.
        :type short_name: str
        """

        self._short_name = short_name

    @property
    def location(self):
        """Gets the location of this Node.


        :return: The location of this Node.
        :rtype: Location
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this Node.


        :param location: The location of this Node.
        :type location: Location
        """
        if location is None:
            raise ValueError(
                "Invalid value for `location`, must not be `None`"
            )  # noqa: E501

        self._location = location

    def set_location(self, location):
        """Sets the location of this Node.

        :param location: The location of this Node.
        :type: Location
        """
        if location is None:
            raise ValueError(
                "Invalid value for `location`, must not be `None`"
            )

        location_handler = LocationHandler()
        self._location = location_handler.import_location_data(location)

        return self.location

    @property
    def ports(self):
        """Gets the ports of this Node.


        :return: The ports of this Node.
        :rtype: List[Port]
        """
        return self._ports

    @ports.setter
    def ports(self, ports):
        """Sets the ports of this Node.


        :param ports: The ports of this Node.
        :type ports: List[Port]
        """
        if ports is None:
            raise ValueError(
                "Invalid value for `ports`, must not be `None`"
            )  # noqa: E501

        self._ports = ports

    def set_ports(self, ports):
        """Sets the ports of this Node.


        :param ports: The ports of this Node.
        :type: list[port]
        """
        if ports is None:
            raise ValueError("Invalid value for `ports`, must not be `None`")

        if self._ports is None:
            self._ports = []

        for port in ports:
            port_handler = PortHandler()
            port_obj = port_handler.import_port_data(port)
            self._ports.append(port_obj)

        return self._ports

    @property
    def private_attributes(self):
        """Gets the private_attributes of this Node.


        :return: The private_attributes of this Node.
        :rtype: List[str]
        """
        return self._private_attributes

    @private_attributes.setter
    def private_attributes(self, private_attributes):
        """Sets the private_attributes of this Node.


        :param private_attributes: The private_attributes of this Node.
        :type private_attributes: List[str]
        """

        self._private_attributes = private_attributes
