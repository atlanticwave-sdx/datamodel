"""""
Checks for Connection objects to be in the expected format.
"""

import logging
from datetime import datetime
from re import match

import pytz

from sdx_datamodel.models.connection import Connection
from sdx_datamodel.models.port import Port

ISO_FORMAT = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[-+]\d{2}:\d{2}"

ISO_TIME_FORMAT = r"(^(?:[1-9]\d{3}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1\d|2[0-8])|(?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[1-9]\d(?:0[48]|[2468][048]|[13579][26])|(?:[2468][048]|[13579][26])00)-02-29)T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:Z|[+-][01]\d:[0-5]\d)$)"  # noqa: E501


class ConnectionValidator:
    """
    The validation class made to validate a Connection request
    """

    def __init__(self, connection):
        if not isinstance(connection, Connection):
            raise ValueError(
                "ConnectionValidator must be passed a Connection object"
            )

        self._connection = connection

        self._logger = logging.getLogger(__name__)

    def is_valid(self) -> bool:
        errors = self.validate(raise_error=True)
        for error in errors:
            self._logger.error(error)
        return not bool(errors)

    def validate(self, raise_error=True) -> [str]:
        errors = self._validate_connection(self._connection)
        if errors and raise_error:
            raise ValueError("\n".join(errors))
        return errors

    def _validate_connection(self, conn: Connection):
        """
        Validate that the connection provided meets the JSON schema.

        A connection must have the following:

            - It must meet object standard

            - It must have the default fields: id, name, ingress_port,
              and egress_port

        :param connection: The connection being evaluated

        :return: A list of any issues in the data.
        """

        errors = []
        errors += self._validate_object_defaults(conn)
        errors += self._validate_port(conn.ingress_port, conn)
        errors += self._validate_port(conn.egress_port, conn)

        if conn.start_time or conn.end_time:
            errors += self._validate_time(conn.start_time, conn.end_time, conn)

        if conn.latency_required:
            errors += self._validate_qos_metrics_value(
                "max_delay", conn.latency_required, 1000
            )

        if conn.bandwidth_required:
            errors += self._validate_qos_metrics_value(
                "min_bw", conn.bandwidth_required, 100
            )

        if conn.max_number_oxps:
            errors += self._validate_qos_metrics_value(
                "max_number_oxps", conn.bandwidth_required, 100
            )
        return errors

    def _validate_qos_metrics_value(self, metric, value, max_value):
        """
        Validate that the QoS Metrics provided meets the XSD standards.

        A connection must have the following:

            - It must meet object default standards.

            - The max_delay must be a number

            - The max_number_oxps must be a number

        :param qos_metrics: The QoS Metrics being evaluated.

        :return: A list of any issues in the data.
        """
        errors = []

        if not isinstance(value, int):
            errors.append(f"{value} {metric} must be a number")
        if not (0 <= value <= max_value):
            errors.append(f"{value} {metric} must be between 0 and 1000")

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
        if not port:
            errors.append(f"{port.__class__.__name__} must exist")

        errors += self._validate_object_defaults(port)

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

    def _validate_time(self, start_time: str, end_time: str, conn: Connection):
        """
        Validate that the time provided meets the XSD standards.

        :param start_time, end_time: time being validated

        :return: A list of any issues in the data.
        """
        utc = pytz.UTC
        errors = []
        # if not match(ISO_TIME_FORMAT, time):
        #    errors.append(f"{time} time needs to be in full ISO format")
        if not start_time:
            start_time = str(datetime.now())
        try:
            start_time_obj = datetime.fromisoformat(start_time)
            start_time = start_time_obj.replace(tzinfo=utc)
            if start_time < datetime.now().replace(tzinfo=utc):
                errors.append(
                    f"{start_time} start_time cannot be before the current time"
                )
        except ValueError:
            errors.append(
                f"{start_time} start_time is not in a valid ISO format"
            )
        if end_time:
            try:
                end_time_obj = datetime.fromisoformat(end_time)
                end_time = end_time_obj.replace(tzinfo=utc)
                if (
                    end_time < datetime.now().replace(tzinfo=utc)
                    or end_time < start_time
                ):
                    errors.append(
                        f"{end_time} end_time cannot be before the current or start time"
                    )
            except ValueError:
                errors.append(
                    f"{end_time} end_time is not in a valid ISO format"
                )

        return errors

    def _validate_object_defaults(self, sdx_object):
        """
        Validate that default fields meets the XSD standards.

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
                f"{sdx_object.__class__.__name__} {sdx_object._name} "
                f"must have a name"
            )
        if not isinstance(sdx_object._name, str):
            errors.append(
                f"{sdx_object.__class__.__name__} {sdx_object._name} "
                f"name must be a string"
            )

        return errors
