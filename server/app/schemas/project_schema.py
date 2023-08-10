from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional
from app.schemas import organization_schema


class ProjectStatus(str, Enum):
    pending = 'pending',
    waiting = 'waiting',
    running = 'running',
    successful = 'successful',
    failed = 'failed',
    error = 'error',
    canceled = 'canceled',
    never_updated = 'never_updated',
    ok = 'ok',
    missing = 'missing'


class SourceControlCredentialType(str, Enum):
    manual = 'manual'
    git = 'git'


class Tool(str, Enum):
    ansible = 'ansible'
    jenkins = 'jenkins'
    terraform = 'terraform'
    playwright = 'playwright'


class ProjectBase(BaseModel):
    name: str
    description: Optional[str]
    source_control_credential_type: SourceControlCredentialType
    tool: Tool
    source_control_url: Optional[str]
    base_path: Optional[str]
    playbook_directory: Optional[str]


class ProjectRequest(ProjectBase):
    organization_id: int


class ProjectResponse(ProjectBase):
    id: int
    project_status: ProjectStatus
    created_at: datetime
    last_modified_at: datetime
    created_by: str
    last_modified_by: str
    organization: organization_schema.OrganizationRelationship

    class Config:
        orm_mode = True


class ProjectRelationship(BaseModel):
    id: int
    name: str
    project_status: ProjectStatus

    class Config:
        orm_mode = True
