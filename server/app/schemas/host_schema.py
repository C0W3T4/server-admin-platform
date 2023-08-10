from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional
from . import organization_schema


class HostStatus(str, Enum):
    alive = 'alive'
    successful = 'successful'
    failed = 'failed'
    unreachable = 'unreachable'


class HostBase(BaseModel):
    description: Optional[str]
    hostname: str
    ipv4: str


class HostRequest(HostBase):
    organization_id: int


class HostResponse(HostBase):
    id: int
    host_status: HostStatus
    created_at: datetime
    last_modified_at: datetime
    created_by: str
    last_modified_by: str
    organization: organization_schema.OrganizationRelationship

    class Config:
        orm_mode = True


class HostRelationship(BaseModel):
    id: int
    hostname: str
    ipv4: str
    host_status: HostStatus

    class Config:
        orm_mode = True
