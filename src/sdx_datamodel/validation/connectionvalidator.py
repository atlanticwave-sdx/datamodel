"""""
Checks for Connection objects to be in the expected format.
"""

import logging
from datetime import datetime
from re import match

import pytz

from sdx_datamodel.models.connection import Connection
from sdx_datamodel.models.port import Port
from sdx_datamodel.parsing.exceptions import (
    AttributeNotSupportedException,
    InvalidVlanRangeException,
    MissingAttributeException,
    ServiceNotSupportedException,
)


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

        if len(errors) > 0:
            return errors

        errors += self._validate_connection_vlan(
            conn.ingress_port.vlan_range, conn.egress_port.vlan_range
        )

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
                "max_number_oxps", conn.max_number_oxps, 100
            )
        return errors

    def _validate_qos_metrics_value(self, metric, value, max_value):
        """
        Validate that the QoS Metrics provided meets the XSD standards.

        A connection must have the following:

            - It must meet object default standards.

            - The max_delay must be a number

            - The max_number_oxps must be a number between 0 and 100

        :param qos_metrics: The QoS Metrics being evaluated.

        :return: A list of any issues in the data.
        """
        errors = []

        if not isinstance(value, int):
            errors.append(
                f"Strict QoS requirements: {value} {metric} must be a number"
            )
        if not (0 <= value <= max_value):
            errors.append(
                f"Strict QoS requirements: {value} {metric} must be between 0 and 1000"
            )

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

        if port.vlan_range is None:
            errors.append(
                f"{port.__class__.__name__} {port._name} must have a vlan"
            )

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

    def _validate_connection_vlan(self, ingress_vlan: str, egress_vlan: str):
        """
        validate VLAN in connection request.

        VLAN is of the following: 1-4095, "100:200", "any", "all" or "untagged"
        """
        errors = []
        if not isinstance(ingress_vlan, str):
            errors.append(
                f"VLAN ({ingress_vlan}) must be a str, but is {type(ingress_vlan)}"
            )
            return errors

        if not isinstance(egress_vlan, str):
            errors.append(
                f"VLAN ({egress_vlan}) must be a str, but is {type(egress_vlan)}"
            )
            return errors

        if ingress_vlan == "all" or egress_vlan == "all":
            if ingress_vlan != "all" or egress_vlan != "all":
                errors.append(
                    "Invalid VLAN: If one VLAN is 'all', the other must also be 'all'"
                )
                return errors

        if ":" in ingress_vlan or ":" in egress_vlan:
            if ingress_vlan != egress_vlan:
                errors.append(
                    f"VLAN ranges must be equal: {ingress_vlan} != {egress_vlan}"
                )
                return errors

        error = self._validate_vlan(ingress_vlan)
        if error:
            errors.append(error)
        error = self._validate_vlan(egress_vlan)
        if error:
            errors.append(error)

        return errors

    def _validate_vlan(self, vlan: str):
        if vlan == "any" or vlan == "untagged":
            return None

        if ":" in vlan:
            v1 = vlan.split(":")[0]
            v2 = vlan.split(":")[1]
        else:
            v2 = v1 = vlan

        if not v1.isdigit() or not v2.isdigit():
            if v1 == v2:
                error = f"VLAN range {vlan} is invalid: {v1} is not a number"
            else:
                error = f"VLAN range {vlan} is invalid: {v1} or {v2} is not a number"
            return error

        v1 = int(v1)
        v2 = int(v2)

        if v1 < 1 or v2 < 1 or v1 > 4095 or v2 > 4095:
            if v1 == v2:
                error = f"VLAN range {vlan} is invalid: {v1} is out of range (1-4095)"
            else:
                error = f"VLAN range {vlan} is invalid: {v1} or {v2} is out of range (1-4095)"
            return error

        if v1 > v2:
            error = f"VLAN range {vlan} is invalid: {v1} > {v2}"
            return error

    def _validate_time(self, start_time: str, end_time: str, conn: Connection):
        """
        Validate that the time provided meets the XSD standards.

        :param start_time, end_time: time being validated

        :return: A list of any issues in the data.
        """
        utc = pytz.UTC
        errors = []
        now = datetime.now().replace(tzinfo=utc)
        if not start_time:
            start_time = str(datetime.now())
        try:
            start_time_obj = datetime.fromisoformat(start_time)
            start_time = start_time_obj.replace(tzinfo=utc)
            if start_time < now:
                errors.append(
                    f"Scheduling not possible: {start_time} start_time cannot be before the current time"
                )

            if (start_time - now).total_seconds() > 300:
                raise AttributeNotSupportedException(
                    f"Scheduling advanced reservation is not supported: start_time {start_time} "
                )
        except ValueError:
            errors.append(
                f"Scheduling not possible: {start_time} start_time is not in a valid ISO format"
            )
        if end_time:
            try:
                end_time_obj = datetime.fromisoformat(end_time)
                end_time = end_time_obj.replace(tzinfo=utc)
                if end_time < now or end_time < start_time:
                    errors.append(
                        f"Scheduling not possible: {end_time} end_time cannot be before the current or start time"
                    )
            except ValueError:
                errors.append(
                    f"Scheduling not possible: {end_time} end_time is not in a valid ISO format"
                )
            raise AttributeNotSupportedException(
                f"Scheduling advanced reservation is not supported: end_time: {end_time} "
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
