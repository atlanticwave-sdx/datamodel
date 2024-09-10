# This module represents AW-SDX connection requests using Pydantic.
# Here we implement Service Provisioning Data Model Specification 1.0,
# available at https://sdx-docs.readthedocs.io.

import math
import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

__all__ = ["ConnectionRequestV1"]


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
            else:
                return value

        # a range like "1:100" is valid.
        pattern = r"(\d+):(\d+)"
        match = re.match(pattern, value)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            if x not in range(1, 4095):
                raise ValueError(f"vlan {x} is invalid")
            if y not in range(1, 4095):
                raise ValueError(f"vlan {y} is invalid")
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
    email: str = Field(frozen=True)


class Scheduling(BaseModel):
    # TODO: use timestamp validation
    start_time: Optional[datetime] = Field(frozen=True, default=None)
    end_time: Optional[datetime] = Field(frozen=True, default=None)


class MinimumBandwidth(BaseModel):
    value: int = Field(frozen=True, default=0)
    strict: bool = Field(frozen=True, default=False)


class MaximumDelay(BaseModel):
    value: int = Field(frozen=True, default=math.inf)
    strict: bool = Field(frozen=True, default=False)


class MaximumOXP(BaseModel):
    value: int = Field(frozen=True, default=math.inf)
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
    def validate_endpoints(cls, value):
        if len(value) < 2:
            raise ValueError(f"not enough endpoints in {value}")

        # TODO: validate that when requested vlan is a range or "all",
        # they must be identical in all endpoints.

        return value
