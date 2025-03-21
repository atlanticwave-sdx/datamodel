# This module represents AW-SDX connection requests using Pydantic.
# Here we implement Service Provisioning Data Model Specification 1.0,
# available at https://sdx-docs.readthedocs.io.

import math
import re
from datetime import datetime
from typing import List, Optional

import pytz
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    PositiveInt,
    RootModel,
    computed_field,
    field_validator,
)

__all__ = [
    "Service",
    "Port",
    "ConnectionRequest",
    "ConnectionRequestV1",
    "ConnectionRequestV0",
]

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
    start_time: Optional[datetime] = Field(frozen=True, default=datetime.now())
    end_time: Optional[datetime] = Field(frozen=True, default=None)

    @field_validator("start_time", "end_time", mode="before")
    def parse_datetime(cls, value):
        """Convert ISO8601 string to datetime if it's a string."""
        if isinstance(value, str):
            if value == "":
                # FIXME: this is a workaround.  One of the test files have
                # start_time = "" and end_time = "", which does not seem
                # to conform to provisioniong spec.  Both start_time and
                # end_time have to be either a timestamp, or absent.
                return None
            try:
                # Parse ISO8601 string and ensure it's timezone-aware
                dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = pytz.UTC.localize(dt)
                return dt
            except ValueError:
                raise ValueError("Invalid ISO8601 datetime format")
        return value

    @field_validator("end_time")
    def check_time_relationship(cls, end_time, info):
        """Validate that end_time is greater than start_time when both are present."""
        start_time = info.data.get("start_time")
        if end_time is not None and start_time is not None:
            if end_time <= start_time:
                raise ValueError("end_time must be greater than start_time")
        return end_time


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


class Service(BaseModel):
    # The l2vpn_ptp of this Service.
    l2vpn_ptp: object = Field(frozen=True, default=None)

    # The l2vpn_ptmp of this Service.
    l2vpn_ptmp: object = Field(frozen=True, default=None)

    # The monitoring_capability of this Service.
    monitoring_capability: str = Field(frozen=True, default=None)

    # The owner of this Service.
    owner: str = Field(frozen=True, default=None)

    # The private_attributes of this Service.
    private_attributes: List[str] = Field(frozen=True, default=None)

    # The provisioning_system of this Service.
    provisioning_system: str = Field(frozen=True, default=None)

    # The provisioning_url of this Service.
    provisioning_url: str = Field(frozen=True, default=None)

    # The vendor of this Service.
    vendor: List[str] = Field(frozen=True, default=None)


class Port(BaseModel):
    # The id of this Port.
    id: str = Field(frozen=True)

    # The name of this Port.
    name: str = Field(frozen=True, default="unknown")

    # The entities of this Port.
    entities: List[str] = Field(frozen=True, default=[])

    # The short_name of this Port.
    short_name: str = Field(frozen=True, default="")

    # The node of this Port.
    node: str = Field(frozen=True, default=None)

    # The vlan range of this Port.
    vlan_range: Optional[str] = Field(frozen=True, default=None)

    # `label` and `label_range` are V0 artifacts.  Should be safe to
    # remove them when we remove v0 connection requests.  See
    # data/requests/v0/test_request_p2p.json for a usage example.
    label: str = Field(frozen=True, default=None)
    label_range: str = Field(frozen=True, default=None)

    # The status of this Port.
    status: str = Field(frozen=True, default=None)

    # The state of this Port.
    state: str = Field(frozen=True, default=None)

    # The nni of this Port.
    nni: str = Field(frozen=True, default=None)

    # The technology/bandwidth of this Port.
    type: str = Field(frozen=True, default=None)

    # The services of this Port.
    services: Service = Field(frozen=True, default=None)

    # The private_attributes of this Port.
    private_attributes: List[str] = Field(frozen=True, default=[])


class ConnectionRequestV1(BaseModel):
    # The id field is not requied by the spec, but PCE needs it, and
    # SDX-Controller computes it when a request arrives.  So we need
    # id to be an assignable field.
    id: Optional[str] = Field(frozen=False, default=None)

    name: str = Field(frozen=True)
    endpoints: List[EndPoint] = Field(frozen=True)

    description: Optional[str] = Field(frozen=True, default=None)
    notifications: Optional[List[NotificationEmail]] = Field(
        frozen=True, default=None
    )
    scheduling: Optional[Scheduling] = Field(frozen=True, default=None)
    qos_metrics: Optional[QoSMetrics] = Field(frozen=True, default=None)

    # Add the properties that PCE needs.
    @computed_field
    @property
    def ingress_port(self) -> Port:
        ep = self.endpoints[0]
        return Port(id=ep.port_id, vlan_range=ep.vlan)

    @computed_field
    @property
    def egress_port(self) -> Port:
        ep = self.endpoints[-1]
        return Port(id=ep.port_id, vlan_range=ep.vlan)

    @computed_field
    @property
    def bandwidth_required(self) -> PositiveInt:
        if self.qos_metrics and self.qos_metrics.min_bw:
            return self.qos_metrics.min_bw.value
        return 0

    @computed_field
    @property
    def latency_required(self) -> PositiveInt:
        if self.qos_metrics and self.qos_metrics.max_delay:
            return self.qos_metrics.max_delay.value
        return math.inf

    @computed_field
    @property
    def start_time(self) -> datetime | None:
        if self.scheduling:
            return self.scheduling.start_time
        return None

    @computed_field
    @property
    def end_time(self) -> datetime | None:
        if self.scheduling:
            return self.scheduling.end_time
        return None

    @computed_field
    @property
    def max_number_oxps(self) -> PositiveInt:
        if self.qos_metrics and self.qos_metrics.max_number_oxps:
            return self.qos_metrics.max_number_oxps.value
        return None

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


class ConnectionRequestV0(BaseModel):
    """
    Backward compatibility for original request format.
    """

    id: str = Field(frozen=True)
    name: str = Field(frozen=True, default=None)

    ingress_port: Port = Field(frozen=True)
    egress_port: Port = Field(frozen=True)

    start_time: Optional[datetime] = Field(frozen=True, default=None)
    end_time: Optional[datetime] = Field(frozen=True, default=None)

    bandwidth_required: Optional[PositiveInt] = Field(frozen=True, default=0)
    latency_required: Optional[PositiveInt] = Field(frozen=True, default=0)


class ConnectionRequest(RootModel):
    """
    A convenience class to validate either version of the request.
    """

    root: ConnectionRequestV1 | ConnectionRequestV0

    def __getattr__(self, name):
        """
        Convenience method to access the root value directly.
        """
        return getattr(self.root, name)
