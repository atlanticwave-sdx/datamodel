# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from sdx_datamodel import util
from sdx_datamodel.models.base_model_ import Model
from sdx_datamodel.models.link_measurement_period import (  # noqa: F401,E501
    LinkMeasurementPeriod,
)
from sdx_datamodel.models.port import Port  # noqa: F401,E501s
from sdx_datamodel.parsing.porthandler import PortHandler


class Link(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(
        self,
        id=None,
        name=None,
        short_name=None,
        ports=None,
        bandwidth=None,
        residual_bandwidth=None,
        latency=None,
        packet_loss=None,
        availability=None,
        status=None,
        state=None,
        private_attributes=None,
        timestamp=None,
        measurement_period=None,
    ):  # noqa: E501
        """Link - a model defined in Swagger

        :param id: The id of this Link.  # noqa: E501
        :type id: str
        :param name: The name of this Link.  # noqa: E501
        :type name: str
        :param short_name: The short_name of this Link.  # noqa: E501
        :type short_name: str
        :param ports: The ports of this Link.  # noqa: E501
        :type ports: List[Port]
        :param bandwidth: The bandwidth of this Link.  # noqa: E501
        :type bandwidth: float
        :param residual_bandwidth: The residual_bandwidth of this Link.  # noqa: E501
        :type residual_bandwidth: float
        :param latency: The latency of this Link.  # noqa: E501
        :type latency: float
        :param packet_loss: The packet_loss of this Link.  # noqa: E501
        :type packet_loss: float
        :param availability: The availability of this Link.  # noqa: E501
        :type availability: float
        :param status: The status of this Link.  # noqa: E501
        :type status: str
        :param state: The state of this Link.  # noqa: E501
        :type state: str
        :param private_attributes: The private_attributes of this Link.  # noqa: E501
        :type private_attributes: List[str]
        :param timestamp: The timestamp of this Link.  # noqa: E501
        :type timestamp: datetime
        :param measurement_period: The measurement_period of this Link.  # noqa: E501
        :type measurement_period: LinkMeasurementPeriod
        """
        self.swagger_types = {
            "id": str,
            "name": str,
            "short_name": str,
            "ports": List[Port],
            "bandwidth": float,
            "residual_bandwidth": float,
            "latency": float,
            "packet_loss": float,
            "availability": float,
            "status": str,
            "state": str,
            "private_attributes": List[str],
            "timestamp": datetime,
            "measurement_period": LinkMeasurementPeriod,
        }

        self.attribute_map = {
            "id": "id",
            "name": "name",
            "short_name": "short_name",
            "ports": "ports",
            "bandwidth": "bandwidth",
            "residual_bandwidth": "residual_bandwidth",
            "latency": "latency",
            "packet_loss": "packet_loss",
            "availability": "availability",
            "status": "status",
            "state": "state",
            "private_attributes": "private_attributes",
            "timestamp": "timestamp",
            "measurement_period": "measurement_period",
        }
        self._id = id
        self._name = name
        self._short_name = short_name
        self._ports = ports  # list of port dicts
        self._bandwidth = bandwidth
        self._residual_bandwidth = residual_bandwidth
        self._latency = latency
        self._packet_loss = packet_loss
        self._availability = availability
        self._status = status
        self._state = state
        self._private_attributes = private_attributes
        self._timestamp = timestamp
        self._measurement_period = measurement_period

    @classmethod
    def from_dict(cls, dikt):
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The link of this Link.  # noqa: E501
        :rtype: Link
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Link.


        :return: The id of this Link.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Link.


        :param id: The id of this Link.
        :type id: str
        """
        if id is None:
            raise ValueError(
                "Invalid value for `id`, must not be `None`"
            )  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this Link.


        :return: The name of this Link.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Link.


        :param name: The name of this Link.
        :type name: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501

        self._name = name

    @property
    def short_name(self):
        """Gets the short_name of this Link.


        :return: The short_name of this Link.
        :rtype: str
        """
        return self._short_name

    @short_name.setter
    def short_name(self, short_name):
        """Sets the short_name of this Link.


        :param short_name: The short_name of this Link.
        :type short_name: str
        """

        self._short_name = short_name

    @property
    def ports(self):
        """Gets the ports of this Link.


        :return: The ports of this Link.
        :rtype: List[Port]
        """
        return self._ports

    @ports.setter
    def ports(self, ports):
        """Sets the ports of this Link.


        :param ports: The ports of this Link.
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
            self._ports.append(port)

        return self.ports

    @property
    def bandwidth(self):
        """Gets the bandwidth of this Link.


        :return: The bandwidth of this Link.
        :rtype: float
        """
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        """Sets the bandwidth of this Link.


        :param bandwidth: The bandwidth of this Link.
        :type bandwidth: float
        """

        self._bandwidth = bandwidth

    @property
    def residual_bandwidth(self):
        """Gets the residual_bandwidth of this Link.


        :return: The residual_bandwidth of this Link.
        :rtype: float
        """
        return self._residual_bandwidth

    @residual_bandwidth.setter
    def residual_bandwidth(self, residual_bandwidth):
        """Sets the residual_bandwidth of this Link.


        :param residual_bandwidth: The residual_bandwidth of this Link.
        :type residual_bandwidth: float
        """

        self._residual_bandwidth = residual_bandwidth

    @property
    def latency(self):
        """Gets the latency of this Link.


        :return: The latency of this Link.
        :rtype: float
        """
        return self._latency

    @latency.setter
    def latency(self, latency):
        """Sets the latency of this Link.


        :param latency: The latency of this Link.
        :type latency: float
        """

        self._latency = latency

    @property
    def packet_loss(self):
        """Gets the packet_loss of this Link.


        :return: The packet_loss of this Link.
        :rtype: float
        """
        return self._packet_loss

    @packet_loss.setter
    def packet_loss(self, packet_loss):
        """Sets the packet_loss of this Link.


        :param packet_loss: The packet_loss of this Link.
        :type packet_loss: float
        """

        self._packet_loss = packet_loss

    @property
    def availability(self):
        """Gets the availability of this Link.


        :return: The availability of this Link.
        :rtype: float
        """
        return self._availability

    @availability.setter
    def availability(self, availability):
        """Sets the availability of this Link.


        :param availability: The availability of this Link.
        :type availability: float
        """

        self._availability = availability

    @property
    def status(self):
        """Gets the status of this Link.


        :return: The status of this Link.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Link.


        :param status: The status of this Link.
        :type status: str
        """

        self._status = status

    @property
    def state(self):
        """Gets the state of this Link.


        :return: The state of this Link.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Link.


        :param state: The state of this Link.
        :type state: str
        """

        self._state = state

    @property
    def private_attributes(self):
        """Gets the private_attributes of this Link.


        :return: The private_attributes of this Link.
        :rtype: List[str]
        """
        return self._private_attributes

    @private_attributes.setter
    def private_attributes(self, private_attributes):
        """Sets the private_attributes of this Link.


        :param private_attributes: The private_attributes of this Link.
        :type private_attributes: List[str]
        """

        self._private_attributes = private_attributes

    @property
    def timestamp(self):
        """Gets the timestamp of this Link.


        :return: The timestamp of this Link.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this Link.


        :param timestamp: The timestamp of this Link.
        :type timestamp: datetime
        """

        self._timestamp = timestamp

    @property
    def measurement_period(self):
        """Gets the measurement_period of this Link.


        :return: The measurement_period of this Link.
        :rtype: LinkMeasurementPeriod
        """
        return self._measurement_period

    @measurement_period.setter
    def measurement_period(self, measurement_period):
        """Sets the measurement_period of this Link.


        :param measurement_period: The measurement_period of this Link.
        :type measurement_period: LinkMeasurementPeriod
        """

        self._measurement_period = measurement_period
