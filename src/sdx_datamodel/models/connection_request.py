# This module represents AW-SDX connection requests using Pydantic.
# Here we implement Service Provisioning Data Model Specification 1.0,
# available at https://sdx-docs.readthedocs.io.

from typing import List, Optional

from pydantic import BaseModel


class EndPoint(BaseModel):
    port_id: str
    vlan: str


class ConnectionRequestV1(BaseModel):
    name: str
    endpoints: List[EndPoint]
