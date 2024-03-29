# coding: utf-8

"""
SDX LC

You can find out more about Swagger at http://swagger.io.

OpenAPI spec version: 1.0.0 Contact: yxin@renci.org Generated by:
https://github.com/swagger-api/swagger-codegen.git
"""

import pprint

import six


class Link(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    swagger_types = {
        "id": "str",
        "name": "str",
        "short_name": "str",
        "nni": "bool",
        "ports": "list[Port]",
        "bandwidth": "float",
        "residual_bandwidth": "float",
        "latency": "float",
        "packet_loss": "float",
        "availability": "float",
        "status": "str",
        "state": "str",
        "private_attributes": "list[str]",
        "timestamp": "datetime",
        "measurement_period": "LinkMeasurementPeriod",
    }

    attribute_map = {
        "id": "id",
        "name": "name",
        "short_name": "short_name",
        "nni": "nni",
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

    def __init__(
        self,
        id=None,
        name=None,
        short_name=None,
        nni=None,
        ports=None,
        bandwidth=None,
        residual_bandwidth=None,
        latency=None,
        packet_loss=None,
        availability=None,
        private_attributes=None,
        timestamp=None,
        measurement_period=None,
    ):
        """Link - a model defined in Swagger"""
        self._id = id
        self._name = name
        self._short_name = short_name
        self._nni = nni
        self._ports = None
        self._bandwidth = bandwidth
        self._residual_bandwidth = residual_bandwidth
        self._latency = latency
        self._packet_loss = packet_loss
        self._availability = availability
        self._state = None
        self._status = None
        self._private_attributes = private_attributes
        self._timestamp = timestamp
        self._measurement_period = measurement_period

        if ports is not None:
            self._ports = self.set_ports(ports)

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
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

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
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

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
        :type: str
        """

        self._short_name = short_name

    @property
    def nni(self):
        """Gets the short_name of this Link.


        :return: The short_name of this Link.
        :rtype: str
        """
        return self._nni

    @nni.setter
    def nni(self, nni):
        """Sets the short_name of this Link.


        :param short_name: The short_name of this Link.
        :type: str
        """

        self._nni = nni

    @property
    def ports(self):
        """Gets the ports of this Link.


        :return: The ports of this Link.
        :rtype: list[Port]
        """
        return self._ports

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

    @ports.setter
    def ports(self, ports):
        """Sets the ports of this Link.


        :param ports: The ports of this Link.
        :type: list[Port]
        """
        if ports is None:
            raise ValueError("Invalid value for `ports`, must not be `None`")

        self._ports = ports

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
        :type: float
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
        :type: float
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
        :type: float
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
        :type: float
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
        :type: float
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
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")

        self._status = status

    @property
    def state(self):
        """Gets the state of this Link.


        :return: The status of this Link.
        :rtype: str
        """
        return self._state

    @status.setter
    def state(self, state):  # noqa: F811
        """Sets the status of this Link.


        :param status: The status of this Link.
        :type: str
        """
        if state is None:
            raise ValueError("Invalid value for `state`, must not be `None`")

        self._state = state

    @property
    def private_attributes(self):
        """Gets the private_attributes of this Link.


        :return: The private_attributes of this Link.
        :rtype: list[str]
        """
        return self._private_attributes

    @private_attributes.setter
    def private_attributes(self, private_attributes):
        """Sets the private_attributes of this Link.


        :param private_attributes: The private_attributes of this Link.
        :type: list[str]
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
        :type: datetime
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
        :type: LinkMeasurementPeriod
        """

        self._measurement_period = measurement_period

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(
                        lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                        value,
                    )
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(Link, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Link):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
