# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from sdx_datamodel import util
from sdx_datamodel.models.base_model_ import Model
from sdx_datamodel.models.link import Link  # noqa: F401,E501
from sdx_datamodel.models.node import Node  # noqa: F401,E501
from sdx_datamodel.models.service import Service  # noqa: F401,E501
from sdx_datamodel.parsing.linkhandler import LinkHandler
from sdx_datamodel.parsing.nodehandler import NodeHandler
from sdx_datamodel.parsing.servicehandler import ServiceHandler

SDX_INSTITUTION_ID = "urn:sdx:topology:"
SDX_TOPOLOGY_ID_prefix = "urn:sdx:topology:"
TOPOLOGY_INITIAL_VERSION = "0.0"


class Topology(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(
        self,
        id=None,
        name=None,
        services=None,
        version=None,
        model_version=None,
        timestamp=None,
        nodes=None,
        links=None,
        private_attributes=None,
    ):  # noqa: E501
        """Topology - a model defined in Swagger

        :param id: The id of this Topology.  # noqa: E501
        :type id: str
        :param name: The name of this Topology.  # noqa: E501
        :type name: str
        :param services: The services of this Topology.  # noqa: E501
        :type services: Service
        :param version: The version of this Topology.  # noqa: E501
        :type version: int
        :param model_version: The model_version of this Topology.  # noqa: E501
        :type model_version: str
        :param timestamp: The timestamp of this Topology.  # noqa: E501
        :type timestamp: datetime
        :param nodes: The nodes of this Topology.  # noqa: E501
        :type nodes: List[Node]
        :param links: The links of this Topology.  # noqa: E501
        :type links: List[Link]
        :param private_attributes: The private_attributes of this Topology.  # noqa: E501
        :type private_attributes: List[str]
        """
        self.swagger_types = {
            "id": str,
            "name": str,
            "services": Service,
            "version": int,
            "model_version": str,
            "timestamp": datetime,
            "nodes": List[Node],
            "links": List[Link],
            "private_attributes": List[str],
        }

        self.attribute_map = {
            "id": "id",
            "name": "name",
            "services": "services",
            "version": "version",
            "model_version": "model_version",
            "timestamp": "timestamp",
            "nodes": "nodes",
            "links": "links",
            "private_attributes": "private_attributes",
        }
        self._id = id
        self._name = name
        if services is None:
            self._services = None
        else:
            self._services = self.set_service(services)
        self._version = version
        self._model_version = model_version
        self._timestamp = timestamp
        self._nodes = []
        self._links = []
        self._port_by_id = {}
        self._nodes = self.set_nodes(nodes)
        self._links = self.set_links(links)
        self._private_attributes = private_attributes

    @classmethod
    def from_dict(cls, dikt):
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The topology of this Topology.  # noqa: E501
        :rtype: Topology
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Topology.


        :return: The id of this Topology.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Topology.


        :param id: The id of this Topology.
        :type id: str
        """
        if id is None:
            raise ValueError(
                "Invalid value for `id`, must not be `None`"
            )  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this Topology.


        :return: The name of this Topology.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Topology.


        :param name: The name of this Topology.
        :type name: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501

        self._name = name

    @property
    def services(self):
        """Gets the services of this Topology.


        :return: The services of this Topology.
        :rtype: Service
        """
        return self._services

    @services.setter
    def services(self, services):
        """Sets the services of this Topology.


        :param services: The services of this Topology.
        :type services: Service
        """

        self._services = services

    def set_service(self, services):
        """parse the service of this Topology.


        :param service: The services of this Topology.
        :type: Service
        """
        if services is None:
            raise ValueError(
                "Invalid value for `services`, must not be `None`"
            )

        service_handler = ServiceHandler()
        self._services = service_handler.import_service_data(services)

        return self.services

    @property
    def version(self):
        """Gets the version of this Topology.


        :return: The version of this Topology.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Topology.


        :param version: The version of this Topology.
        :type version: int
        """
        if version is None:
            raise ValueError(
                "Invalid value for `version`, must not be `None`"
            )  # noqa: E501

        self._version = version

    @property
    def model_version(self):
        """Gets the model_version of this Topology.


        :return: The model_version of this Topology.
        :rtype: str
        """
        return self._model_version

    @model_version.setter
    def model_version(self, model_version):
        """Sets the model_version of this Topology.


        :param model_version: The model_version of this Topology.
        :type model_version: str
        """

        self._model_version = model_version

    @property
    def timestamp(self):
        """Gets the timestamp of this Topology.


        :return: The timestamp of this Topology.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this Topology.


        :param timestamp: The timestamp of this Topology.
        :type timestamp: datetime
        """
        if timestamp is None:
            raise ValueError(
                "Invalid value for `timestamp`, must not be `None`"
            )  # noqa: E501

        self._timestamp = timestamp

    @property
    def nodes(self):
        """Gets the nodes of this Topology.


        :return: The nodes of this Topology.
        :rtype: List[Node]
        """
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        """Sets the nodes of this Topology.


        :param nodes: The nodes of this Topology.
        :type nodes: List[Node]
        """
        if nodes is None:
            raise ValueError(
                "Invalid value for `nodes`, must not be `None`"
            )  # noqa: E501

        self._nodes = nodes
        self._update_port_by_id(nodes)

    def set_nodes(self, nodes):
        """Sets the nodes of this Topology.


        :param nodes: The nodes of this Topology.
        :type: list[Node]
        """
        if nodes is None:
            raise ValueError("Invalid value for `nodes`, must not be `None`")

        for node in nodes:
            node_handler = NodeHandler()
            node_obj = node_handler.import_node_data(node)
            self._nodes.append(node_obj)
            self._update_port_by_id([node_obj])

        return self.nodes

    def remove_node(self, node_id):
        for node in list(self._nodes):
            if node.id == node_id:
                self._nodes.remove(node)
                for port in node.ports:
                    self._port_by_id.pop(port.id, None)

    def add_nodes(self, node_objects):
        """add the nodes to this Topology.
        :param node_objects: a list of node objects
        """

        self._nodes.extend(node_objects)
        self._update_port_by_id(node_objects)

    def _update_port_by_id(self, nodes):
        """Update _port_by_id dict."""
        for node in nodes:
            for port in node.ports:
                self._port_by_id[port.id] = port

    def add_node(self, node_object):
        """add a node to this Topology.
        :param node_objecs: a node object
        """
        self._nodes.extend(node_object)
        self._update_port_by_id([node_object])

    def get_node_by_port(self, aPort):
        for node in self._nodes:
            ports = node.ports
            for port in ports:
                if port.id == aPort:
                    return node

        return None

    def get_port_by_link(self, n1_id, n2_id):
        for x in self._links:
            # print("--------")
            # print(x.ports[0]['node'])
            # print(x.ports[1]['node'])
            port_id_0 = (
                x.ports[0] if isinstance(x.ports[0], str) else x.ports[0]["id"]
            )
            port_id_1 = (
                x.ports[1] if isinstance(x.ports[1], str) else x.ports[1]["id"]
            )
            port_0 = self._port_by_id[port_id_0]
            port_1 = self._port_by_id[port_id_1]
            if port_0.node == n1_id and port_1.node == n2_id:
                return n1_id, port_0.to_dict(), n2_id, port_1.to_dict()
            if port_0.node == n2_id and port_1.node == n1_id:
                return n1_id, port_1.to_dict(), n2_id, port_0.to_dict()

    def get_link_by_port_id(self, port_id_0, port_id_1):
        for link in self._links:
            p_0 = (
                link.ports[0]
                if isinstance(link.ports[0], str)
                else link.ports[0]["id"]
            )
            p_1 = (
                link.ports[1]
                if isinstance(link.ports[1], str)
                else link.ports[1]["id"]
            )
            if (p_0 == port_id_0 and p_1 == port_id_1) or (
                p_0 == port_id_1 and p_1 == port_id_0
            ):
                # print(f"found link: {link} from {port_id_0} to {port_id_1}")
                return link

    def get_link_by_id(self, link_id):
        for link in self._links:
            if link.id == link_id:
                return link

    def has_node_by_id(self, id):
        for node in self._nodes:
            if id == node.id:
                return True
        return False

    def get_node_by_id(self, id):
        for node in self._nodes:
            if id == node.id:
                return node
        return None

    @property
    def links(self):
        """Gets the links of this Topology.


        :return: The links of this Topology.
        :rtype: List[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this Topology.


        :param links: The links of this Topology.
        :type links: List[Link]
        """
        if links is None:
            raise ValueError(
                "Invalid value for `links`, must not be `None`"
            )  # noqa: E501

        self._links = links

    def set_links(self, links):
        """Sets the links of this Topology.

        :param links: The links of this Topology, in list of JSON str.
        :type: list[Link]
        """
        if links is None:
            raise ValueError("Invalid value for `links`, must not be `None`")

        for link in links:
            link_handler = LinkHandler()
            link_obj = link_handler.import_link_data(link)
            self._links.append(link_obj)

        return self.links

    def remove_link(self, link_id):
        for link in list(self._links):
            if link.id == link_id:
                self._links.remove(link)

    def add_links(self, link_objects):
        """add the links to this Topology.
        :param link_objects: a list of link objects
        """

        self._links.extend(link_objects)

    def get_link_by_id(self, id):
        for link in self._links:
            if id == link.id:
                return link
        return None

    @property
    def private_attributes(self):
        """Gets the private_attributes of this Topology.


        :return: The private_attributes of this Topology.
        :rtype: List[str]
        """
        return self._private_attributes

    @private_attributes.setter
    def private_attributes(self, private_attributes):
        """Sets the private_attributes of this Topology.


        :param private_attributes: The private_attributes of this Topology.
        :type private_attributes: List[str]
        """

        self._private_attributes = private_attributes

    def nodes_id(self):
        return [node.id for node in self._nodes]

    def links_id(self):
        return [link.id for link in self._links]

    def ports_id(self):
        return [port.id for port in self._port_by_id.values()]
