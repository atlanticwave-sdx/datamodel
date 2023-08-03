# coding: utf-8

"""
SDX LC

You can find out more about Swagger at
[http://swagger.io](http://swagger.io) or on [irc.freenode.net,
#swagger](http://swagger.io/irc/).  

OpenAPI spec version: 1.0.0
Contact: yxin@renci.org
Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint

import six


class Port(object):
    """NOTE: This class is auto generated by the swagger code
    generator program.

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
        "short_name": "str",
        "node": "str",
        "label_range": "list[str]",
        "status": "str",
        "state": "str",
        "private_attributes": "list[str]",
    }

    attribute_map = {
        "id": "id",
        "name": "name",
        "short_name": "short_name",
        "node": "node",
        "label_range": "label_range",
        "status": "status",
        "state": "state",
        "private_attributes": "private_attributes",
    }

    def __init__(
        self,
        id=None,
        name=None,
        short_name=None,
        node=None,
        label_range=None,
        status=None,
        private_attributes=None,
    ):
        """Port - a model defined in Swagger"""
        self._id = None
        self._name = None
        self._short_name = None
        self._node = None
        self._label_range = None
        self._status = None
        self._private_attributes = None
        self._id = id
        self._name = name
        if short_name is not None:
            self._short_name = short_name
        self._node = node
        if label_range is not None:
            self._label_range = label_range
        self._status = status
        if private_attributes is not None:
            self._private_attributes = private_attributes

    # def __init__(self, port:dict):
    #    self.__init__(id=id, name=port['name'],short_name=port['short_name'], node=port['node'],
    #    label_range=port['label_range'], status=None, private_attributes=port['private_attributes'])

    @property
    def id(self):
        """Gets the id of this Port.


        :return: The id of this Port.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Port.


        :param id: The id of this Port.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def name(self):
        """Gets the name of this Port.


        :return: The name of this Port.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Port.


        :param name: The name of this Port.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def short_name(self):
        """Gets the short_name of this Port.


        :return: The short_name of this Port.
        :rtype: str
        """
        return self._short_name

    @short_name.setter
    def short_name(self, short_name):
        """Sets the short_name of this Port.


        :param short_name: The short_name of this Port.
        :type: str
        """

        self._short_name = short_name

    @property
    def node(self):
        """Gets the node of this Port.


        :return: The node of this Port.
        :rtype: str
        """
        return self._node

    @node.setter
    def node(self, node):
        """Sets the node of this Port.


        :param node: The node of this Port.
        :type: str
        """
        if node is None:
            raise ValueError("Invalid value for `node`, must not be `None`")

        self._node = node

    @property
    def label_range(self):
        """Gets the label_range of this Port.


        :return: The label_range of this Port.
        :rtype: list[str]
        """
        return self._label_range

    @label_range.setter
    def label_range(self, label_range):
        """Sets the label_range of this Port.


        :param label_range: The label_range of this Port.
        :type: list[str]
        """

        self._label_range = label_range

    @property
    def status(self):
        """Gets the status of this Port.


        :return: The status of this Port.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Port.


        :param status: The status of this Port.
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")

        self._status = status

    @property
    def state(self):
        """Gets the state of this Port.


        :return: The state of this Port.
        :rtype: str
        """
        return self._state

    @status.setter
    def state(self, state):  # noqa: F811
        """Sets the state of this Port.


        :param state: The state of this Port.
        :type: str
        """
        if state is None:
            raise ValueError("Invalid value for `state`, must not be `None`")

        self._state = state

    @property
    def private_attributes(self):
        """Gets the private_attributes of this Port.


        :return: The private_attributes of this Port.
        :rtype: list[str]
        """
        return self._private_attributes

    @private_attributes.setter
    def private_attributes(self, private_attributes):
        """Sets the private_attributes of this Port.


        :param private_attributes: The private_attributes of this Port.
        :type: list[str]
        """

        self._private_attributes = private_attributes

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
        if issubclass(Port, dict):
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
        if not isinstance(other, Port):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
