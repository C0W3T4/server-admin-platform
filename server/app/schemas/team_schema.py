from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from . import tower_schema


class TeamBase(BaseModel):
    name: str
    description: Optional[str]


class TeamRequest(TeamBase):
    pass


class TeamResponse(TeamBase):
    id: int
    created_at: datetime
    last_modified_at: datetime
    created_by: str
    last_modified_by: str
    tower: tower_schema.TowerRelationship

    class Config:
        orm_mode = True


class TeamRelationship(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
