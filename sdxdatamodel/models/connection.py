# coding: utf-8

"""
    SDX LC

    You can find out more about Swagger at [http://swagger.io](http://swagger.io) or on [irc.freenode.net, #swagger](http://swagger.io/irc/).   # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: yxin@renci.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401
import six

from sdxdatamodel.parsing.porthandler import PortHandler


class Connection(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

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
        "ingress_port": "Port",
        "egress_port": "Port",
        "quantity": "int",
        "start_time": "datetime",
        "end_time": "datetime",
        "status": "str",
    }

    attribute_map = {
        "id": "id",
        "name": "name",
        "ingress_port": "ingress_port",
        "egress_port": "egress_port",
        "quantity": "quantity",
        "start_time": "start_time",
        "end_time": "end_time",
        "bandwidth": "float",
        "latency": "float",
        "latency": "float",
        "status": "status",
    }

    def __init__(
        self,
        id=None,
        name=None,
        ingress_port=None,
        egress_port=None,
        bandwidth=None,
        latency=None,
        quantity=None,
        start_time=None,
        end_time=None,
        status=None,
        complete=False,
    ):  # noqa: E501

        self._id = id
        self._name = name
        self._quantity = None
        self._start_time = None
        self._end_time = None
        self._status = None
        self._bandwidth = (None,)
        self._latency = (None,)
        self.set_ingress_port(ingress_port)
        self.set_egress_port(egress_port)
        if bandwidth is not None:
            self._bandwidth = bandwidth
        if latency is not None:
            self._latency = latency
        if quantity is not None:
            self._quantity = quantity
        if start_time is not None:
            self._start_time = start_time
        if end_time is not None:
            self._end_time = end_time
        if status is not None:
            self._status = status

    @property
    def id(self):
        """Gets the id of this Connection.  # noqa: E501


        :return: The id of this Connection.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Connection.


        :param id: The id of this Connection.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError(
                "Invalid value for `id`, must not be `None`"
            )  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this Connection.  # noqa: E501


        :return: The name of this Connection.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Connection.


        :param name: The name of this Connection.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501

        self._name = name

    @property
    def ingress_port(self):
        """Gets the ingress_port of this Connection.  # noqa: E501


        :return: The ingress_port of this Connection.  # noqa: E501
        :rtype: Port
        """
        return self._ingress_port

    # setter
    def set_ingress_port(self, ingress_port):
        """Sets the ingress_port of this Connection.


        :param ingress_port: The ingress_port of this Connection.  # noqa: E501
        :type: Port
        """
        if ingress_port is None:
            raise ValueError(
                "Invalid value for `ingress_port`, must not be `None`"
            )  # noqa: E501

        port_handler = PortHandler()
        self._ingress_port = port_handler.import_port_data(ingress_port)

        return self.ingress_port

    @property
    def egress_port(self):
        """Gets the egress_port of this Connection.  # noqa: E501


        :return: The egress_port of this Connection.  # noqa: E501
        :rtype: Port
        """
        return self._egress_port

    # setter
    def set_egress_port(self, egress_port):
        """Sets the egress_port of this Connection.


        :param egress_port: The egress_port of this Connection.  # noqa: E501
        :type: Port
        """
        if egress_port is None:
            raise ValueError(
                "Invalid value for `egress_port`, must not be `None`"
            )  # noqa: E501

        port_handler = PortHandler()
        self._egress_port = port_handler.import_port_data(egress_port)

        return self.egress_port

    @property
    def quantity(self):
        """Gets the quantity of this Connection.  # noqa: E501


        :return: The quantity of this Connection.  # noqa: E501
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this Connection.


        :param quantity: The quantity of this Connection.  # noqa: E501
        :type: int
        """

        self._quantity = quantity

    @property
    def bandwidth(self):
        """Gets the quantity of this Connection.  # noqa: E501


        :return: The quantity of this Connection.  # noqa: E501
        :rtype: float
        """
        return self._bandwidth

    def set_bandwidth(self, bw):
        """Sets the bw of this Connection.


        :param bw: The bw of this Connection.  # noqa: E501
        :type: float
        """

        self._bandwidth = bw

    @property
    def latency(self):
        """Gets the latency of this Connection.  # noqa: E501


        :return: The latency of this Connection.  # noqa: E501
        :rtype: float
        """
        return self._latency

    def set_latency(self, latency):
        """Sets the latency of this Connection.


        :param bw: The latency of this Connection.  # noqa: E501
        :type: float
        """

        self._latency = latency

    @property
    def start_time(self):
        """Gets the start_time of this Connection.  # noqa: E501


        :return: The start_time of this Connection.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this Connection.


        :param start_time: The start_time of this Connection.  # noqa: E501
        :type: datetime
        """

        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this Connection.  # noqa: E501


        :return: The end_time of this Connection.  # noqa: E501
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this Connection.


        :param end_time: The end_time of this Connection.  # noqa: E501
        :type: datetime
        """

        self._end_time = end_time

    @property
    def status(self):
        """Gets the status of this Connection.  # noqa: E501

        Connection Status  # noqa: E501

        :return: The status of this Connection.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Connection.

        Connection Status  # noqa: E501

        :param status: The status of this Connection.  # noqa: E501
        :type: str
        """
        allowed_values = [
            "success",
            "fail",
            "scheduled",
            "provisioining",
        ]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}".format(  # noqa: E501
                    status, allowed_values
                )
            )

        self._status = status

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
        if issubclass(Connection, dict):
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
        if not isinstance(other, Connection):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
