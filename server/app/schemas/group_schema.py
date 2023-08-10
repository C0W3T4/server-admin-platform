from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from . import organization_schema


class GroupBase(BaseModel):
    name: str
    description: Optional[str]


class GroupRequest(GroupBase):
    organization_id: int


class GroupResponse(GroupBase):
    id: int
    created_at: datetime
    last_modified_at: datetime
    created_by: str
    last_modified_by: str
    organization: organization_schema.OrganizationRelationship

    class Config:
        orm_mode = True


class GroupRelationship(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
