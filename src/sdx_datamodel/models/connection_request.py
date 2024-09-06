# This module represents AW-SDX connection requests using Pydantic.
# Here we implement Service Provisioning Data Model Specification 1.0,
# available at https://sdx-docs.readthedocs.io.

import re

from typing import List, Optional

from pydantic import BaseModel, field_validator

__all__ = ["ConnectionRequestV1"]


class EndPoint(BaseModel):
    port_id: str
    vlan: str

    @field_validator("vlan")
    @classmethod
    def validate_vlan(cls, value: str) -> str:
        # an integer like "100" is valid, and it has to be in [1,4095]
        # range.
        if EndPoint.is_integer(value):
            if int(value) not in range(1, 4095):
                raise ValueError(f"vlan {value} is not in [1,4095] range")
            else:
                return value.title()

        # a range like "1:100" is valid.
        if ":" in value:
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
                return value.title()
            else:
                raise ValueError(f"vlan {value} is an invalid range")

        # "any", "all", and "untagged" also are valid.
        if value not in ("any", "all", "untagged"):
            raise ValueError(f"VLAN {value} is not valid")
        else:
            return value.title()

        raise ValueError(f"vlan {value} is invalid")

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
