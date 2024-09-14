# This module represents AW-SDX connection requests using Pydantic.
# Here we implement Service Provisioning Data Model Specification 1.0,
# available at https://sdx-docs.readthedocs.io.

import math
import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, PositiveInt, field_validator

__all__ = ["ConnectionRequestV1", "ConnectionRequestV0"]

# Regular expression used for matching VLAN ranges like "100:200".
VLAN_RANGE_PATTERN = r"(\d+):(\d+)"


class EndPoint(BaseModel):
    port_id: str = Field(frozen=True)
    vlan: str = Field(frozen=True)

    @field_validator("vlan")
    @classmethod
    def validate_vlan(cls, value: str) -> str:
        # an integer like "100" is valid, and it has to be in [1,4095]
        # range.
        if EndPoint.is_integer(value):
            if int(value) not in range(1, 4095):
                raise ValueError(f"vlan {value} is not in [1,4095] range")
            return value

        # a range like "1:100" is valid.
        match = re.match(VLAN_RANGE_PATTERN, value)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            if x not in range(1, 4095):
                raise ValueError(f"vlan {x} is invalid: not in [1,4095] range")
            if y not in range(1, 4095):
                raise ValueError(f"vlan {y} is invalid: not in [1,4095] range")
            if x > y:
                raise ValueError(f"vlan {value} is invalid: {x} > {y}")
            # this range is probably okay.
            return value

        # "any", "all", and "untagged" also are valid.
        if value not in ("any", "all", "untagged"):
            raise ValueError(f"VLAN {value} is not valid")

        # By now we should have have exhausted all possible checks;
        # just return the value.
        return value

    @classmethod
    def is_integer(cls, value) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False


class NotificationEmail(BaseModel):
    # TODO: use email validation
    email: EmailStr = Field(frozen=True)


class Scheduling(BaseModel):
    # TODO: use timestamp validation
    start_time: Optional[datetime] = Field(frozen=True, default=None)
    end_time: Optional[datetime] = Field(frozen=True, default=None)


class MinimumBandwidth(BaseModel):
    value: PositiveInt = Field(frozen=True, default=0)
    strict: bool = Field(frozen=True, default=False)


class MaximumDelay(BaseModel):
    value: PositiveInt = Field(frozen=True, default=math.inf)
    strict: bool = Field(frozen=True, default=False)


class MaximumOXP(BaseModel):
    value: PositiveInt = Field(frozen=True, default=math.inf)
    strict: bool = Field(frozen=True, default=False)


class QoSMetrics(BaseModel):
    min_bw: Optional[MinimumBandwidth] = Field(frozen=True, default=None)
    max_delay: Optional[MaximumDelay] = Field(frozen=True, default=None)
    max_number_oxps: Optional[MaximumOXP] = Field(frozen=True, default=None)


class ConnectionRequestV1(BaseModel):
    name: str = Field(frozen=True)
    endpoints: List[EndPoint] = Field(frozen=True)

    description: Optional[str] = Field(frozen=True, default=None)
    notifications: Optional[List[NotificationEmail]] = Field(
        frozen=True, default=None
    )
    scheduling: Optional[Scheduling] = Field(frozen=True, default=None)
    qos_metrics: Optional[QoSMetrics] = Field(frozen=True, default=None)

    @field_validator("endpoints")
    @classmethod
    def validate_endpoints(cls, endpoints):
        if len(endpoints) < 2:
            raise ValueError(f"not enough endpoints in {endpoints}")

        vlans = [endpoint.vlan for endpoint in endpoints]

        # If one endpoint has the VLAN range or option “all”, all
        # endpoints must have the same value.
        if "all" in vlans and not all(map(lambda x: x == "all", vlans)):
            raise ValueError(
                f"all vlans requested, but not consistently: {vlans}"
            )

        def is_range(value):
            """
            match a pattern like "100:200"
            """
            return bool(re.match(VLAN_RANGE_PATTERN, value))

        # When one endpoint has the VLAN range option in use, all
        # other endpoint(s) must have the same VLAN range.
        if any(map(lambda x: is_range(x), vlans)) and len(set(vlans)) != 1:
            raise ValueError(
                f"range of vlans requested, but not consistently: {vlans}"
            )

        return endpoints


class ConnectionRequestV0Port(BaseModel):
    """
    Backward compatibility for original request format.
    """

    id: str = Field(frozen=True)
    name: str = Field(frozen=True)
    short_name: str = Field(frozen=True, default=None)
    label: str = Field(frozen=True, default=None)
    label_range: str = Field(frozen=True, default=None)
    node: Optional[str] = Field(frozen=True, default=None)
    status: Optional[str] = Field(frozen=True, default=None)


class ConnectionRequestV0(BaseModel):
    """
    Backward compatibility for original request format.
    """

    id: str = Field(frozen=True)
    name: str = Field(frozen=True, default=None)

    ingress_port: ConnectionRequestV0Port = Field(frozen=True)
    egress_port: ConnectionRequestV0Port = Field(frozen=True)

    start_time: Optional[datetime] = Field(frozen=True, default=None)
    end_time: Optional[datetime] = Field(frozen=True, default=None)

    bandwidth_required: Optional[PositiveInt] = Field(
        frozen=True, default=math.inf
    )
    latency_required: Optional[PositiveInt] = Field(frozen=True, default=0)
