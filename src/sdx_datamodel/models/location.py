# coding: utf-8

"""
SDX LC

You can find out more about Swagger at http://swagger.io.

OpenAPI spec version: 1.0.0
Contact: yxin@renci.org
Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint

import six


class Location(object):
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
        "address": "str",
        "latitude": "float",
        "longitude": "float",
    }

    attribute_map = {
        "address": "address",
        "latitude": "latitude",
        "longitude": "longitude",
    }

    def __init__(self, address=None, latitude=None, longitude=None):
        """Location - a model defined in Swagger"""
        self._id = "location"
        self._name = "location"
        self._address = None
        self._latitude = None
        self._longitude = None
        self.discriminator = None
        if address is not None:
            self._address = address
        if latitude is not None:
            self._latitude = latitude
        if longitude is not None:
            self._longitude = longitude

    @property
    def address(self):
        """Gets the address of this Location.


        :return: The address of this Location.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this Location.


        :param address: The address of this Location.
        :type: str
        """

        self._address = address

    @property
    def latitude(self):
        """Gets the latitude of this Location.


        :return: The latitude of this Location.
        :rtype: float
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        """Sets the latitude of this Location.


        :param latitude: The latitude of this Location.
        :type: float
        """

        self._latitude = latitude

    @property
    def longitude(self):
        """Gets the longitude of this Location.


        :return: The longitude of this Location.
        :rtype: float
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        """Sets the longitude of this Location.


        :param longitude: The longitude of this Location.
        :type: float
        """

        self._longitude = longitude

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
        if issubclass(Location, dict):
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
        if not isinstance(other, Location):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
