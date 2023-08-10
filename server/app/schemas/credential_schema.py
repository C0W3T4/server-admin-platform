from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional
from . import organization_schema


class CredentialType(str, Enum):
    machine = 'machine'
    source_control = 'source_control'


class CredentialBase(BaseModel):
    name: str
    description: Optional[str]
    username: str
    port: int
    credential_type: CredentialType


class CredentialRequest(CredentialBase):
    password: str
    ssh_key: Optional[str]
    organization_id: int


class CredentialUpdateRequest(CredentialBase):
    ssh_key: Optional[str]
    organization_id: int


class CredentialResponse(CredentialBase):
    id: int
    created_at: datetime
    last_modified_at: datetime
    created_by: str
    last_modified_by: str
    organization: organization_schema.OrganizationRelationship

    class Config:
        orm_mode = True


class CredentialRelationship(BaseModel):
    id: int
    name: str
    username: str

    class Config:
        orm_mode = True
