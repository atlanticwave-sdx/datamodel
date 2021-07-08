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

class LinkMeasurementPeriod(object):
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
        'period': 'float',
        'time_unit': 'str'
    }

    attribute_map = {
        'period': 'period',
        'time_unit': 'time_unit'
    }

    def __init__(self, period=None, time_unit=None):  # noqa: E501
        """LinkMeasurementPeriod - a model defined in Swagger"""  # noqa: E501
        self._period = None
        self._time_unit = None
        self.discriminator = None
        if period is not None:
            self.period = period
        if time_unit is not None:
            self.time_unit = time_unit

    @property
    def period(self):
        """Gets the period of this LinkMeasurementPeriod.  # noqa: E501


        :return: The period of this LinkMeasurementPeriod.  # noqa: E501
        :rtype: float
        """
        return self._period

    @period.setter
    def period(self, period):
        """Sets the period of this LinkMeasurementPeriod.


        :param period: The period of this LinkMeasurementPeriod.  # noqa: E501
        :type: float
        """

        self._period = period

    @property
    def time_unit(self):
        """Gets the time_unit of this LinkMeasurementPeriod.  # noqa: E501


        :return: The time_unit of this LinkMeasurementPeriod.  # noqa: E501
        :rtype: str
        """
        return self._time_unit

    @time_unit.setter
    def time_unit(self, time_unit):
        """Sets the time_unit of this LinkMeasurementPeriod.


        :param time_unit: The time_unit of this LinkMeasurementPeriod.  # noqa: E501
        :type: str
        """

        self._time_unit = time_unit

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(LinkMeasurementPeriod, dict):
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
        if not isinstance(other, LinkMeasurementPeriod):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
