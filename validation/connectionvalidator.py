"""""
--------------------------------------------------------------------
Synopsis: A validation class to evaluate that the supplied Connection object contains expected data format
"""
from collections.abc import Iterable
from datetime import *
from models import Connection, Port
from re import match

ISO_FORMAT = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[-+]\d{2}:\d{2}'

class ConnectionValidator:
    """
    The validation class made to validate a Connection request
    """
    def __init__(self):
        super().__init__()
        self._connection = None

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def set_connection(self, conn):
        if not isinstance(conn, Connection):
            raise ValueError('The Validator must be passed a Connection object')
        self._connection = conn

    @property
    def is_valid(self):
        errors = self.validate(self._connection, raise_error=True)
        for error in errors:
            print(error)
        return not bool(errors)

    def validate(self, conn=None, raise_error=True):
        if not conn and self._connection:
            conn = self._connection
        errors = self._validate_connection(conn)
        if errors and raise_error:
            raise ValueError('\n'.join(errors))
        return errors

    def _validate_connection(self, conn: Connection):
        """
        Validate that the connection provided meets the JSON schema.
        A connection must have the following:
         - It must meet object standard
         - It must have the default fields: id, name, ingress_port, and egress_port
        :param connection: The connection being evaluated
        :return: A list of any issues in the data.
        """
        errors = []
        errors += self._validate_object_defaults(conn)
        
        for ingress_port in conn.ingress_port:
            errors += self._validate_port(ingress_port, conn)
        for egress_port in conn.egress_port:
            errors += self._validate_port(egress_port, conn)
        for start_time in conn.start_time:
            errors += self._validate_time(start_time, conn)
        for end_time in conn.end_time:
            errors += self._validate_time(end_time, conn)
        return errors

    def _validate_port(self, port: Port, conn: Connection):
        """
        Validate that the port provided meets the XSD standards.
        A port must have the following:
         - It must meet object default standards.
         - A port must belong to a topology
         - The node is optional
        :param port: The port being evaluated.
        :param topology: The Topology.
        :return: A list of any issues in the data.
        """
        errors = []
        errors += self._validate_object_defaults(port)

        if not port:
            errors.append('{} must exist'.format(port.__class__.__name__))

        """
        node = find_node(port,topology)
        if topology and node not in topology.nodes:
            errors.append(
                'listed node id {} does not exist in parent Topology {}'.format(
                    node.id, node, topology.id
                )
            )
        """
        return errors

    def _validate_time(self, time: datetime, conn: Connection):
        """
        Validate that the time provided meets the XSD standards.
        A port must have the following:
         - It must meet object default standards.
         - A link can only connect to 2 nodes
         - The nodes that a link is connected to must be in the parent Topology's nodes list
        :param time: time being validated
        :return: A list of any issues in the data.
        """
        errors = []
        pass

    def _validate_object_defaults(self, sdx_object):
        """
        Validate that the object provided default fields meets the XSD standards.
        The object must have the following:
         - The object must have an ID
         - The object ID must be a string
         - The object must have a name
         - The object name must be a string
         - If the object has a short name, it must be a string
         - If the object has a version, it must be a string in ISO format
         - All the additional properties on the object are proper
        :param sdx_object: The sdx Model Object being evaluated.
        :return: A list of any issues in the data.
        """
        errors = []
        if not sdx_object._id:
            errors.append('{} must have an ID'.format(sdx_object.__class__.__name__))
        if not isinstance(sdx_object._id, str):
            errors.append('{} ID must be a string'.format(sdx_object.__class__.__name__))
        if not sdx_object._name:
            errors.append(
                '{} {} must have a name'.format(
                    sdx_object.__class__.__name__, sdx_object._name,
                )
            )
        if not isinstance(sdx_object._name, str):
            errors.append(
                '{} {} name must be a String'.format(
                    sdx_object.__class__.__name__, sdx_object._name,
                )
            )

        return errors