from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional
from app.schemas import inventory_schema, organization_schema, project_schema, credential_schema


class Verbosity(str, Enum):
    zero = '0'
    one = 'v'
    two = 'vv'
    three = 'vvv'
    four = 'vvvv'
    five = 'vvvvv'
    six = 'vvvvvv'


class LaunchType(str, Enum):
    run = 'run'
    check = 'check'


class TemplateBase(BaseModel):
    name: str
    description: Optional[str]
    launch_type: LaunchType
    playbook_name: str
    limit: Optional[str]
    privilege_escalation: Optional[bool]
    verbosity: Optional[Verbosity]
    forks: Optional[int]
    extra_vars: Optional[str]


class TemplateRequest(TemplateBase):
    inventory_id: int
    project_id: int
    credential_id: int
    organization_id: int


class TemplateResponse(TemplateBase):
    id: int
    created_at: datetime
    last_modified_at: datetime
    created_by: str
    last_modified_by: str
    inventory: inventory_schema.InventoryResponse
    project: project_schema.ProjectResponse
    credential: credential_schema.CredentialResponse
    organization: organization_schema.OrganizationRelationship

    class Config:
        orm_mode = True


class TemplateRelationship(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
