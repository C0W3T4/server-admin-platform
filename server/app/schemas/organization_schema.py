from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from . import tower_schema


class OrganizationBase(BaseModel):
    name: str
    description: Optional[str]


class OrganizationRequest(OrganizationBase):
    pass


class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime
    last_modified_at: datetime
    created_by: str
    last_modified_by: str
    tower: tower_schema.TowerRelationship

    class Config:
        orm_mode = True


class OrganizationRelationship(BaseModel):
    id: int
    name: str
    tower_id: int

    class Config:
        orm_mode = True
