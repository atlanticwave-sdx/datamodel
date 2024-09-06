# This module represents AW-SDX connection requests using Pydantic.
# Here we implement Service Provisioning Data Model Specification 1.0,
# available at https://sdx-docs.readthedocs.io.

from typing import List, Optional

from pydantic import BaseModel, field_validator

__all__ = ["ConnectionRequestV1"]


class EndPoint(BaseModel):
    port_id: str
    vlan: str

    @field_validator("vlan")
    @classmethod
    def validate_vlan(cls, value: str) -> str:
        if EndPoint.is_integer(value) and int(value) not in range(1, 4095):
            raise ValueError(f"{value} is not in [1,4095] range")

        return value.title()

    @classmethod
    def is_integer(cls, value) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False


class ConnectionRequestV1(BaseModel):
    name: str
    endpoints: List[EndPoint]
