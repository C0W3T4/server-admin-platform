from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from . import organization_schema, template_schema


class JobStatus(str, Enum):
    pending = 'pending'
    waiting = 'waiting'
    running = 'running'
    successful = 'successful'
    failed = 'failed'


class JobBase(BaseModel):
    pass


class JobRequest(JobBase):
    template_id: int
    organization_id: int


class JobResponse(JobBase):
    id: int
    job_status: JobStatus
    started_at: datetime
    finished_at: datetime
    launched_by: str
    output: str
    template: template_schema.TemplateResponse
    organization: organization_schema.OrganizationRelationship

    class Config:
        orm_mode = True
