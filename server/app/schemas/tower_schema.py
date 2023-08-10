from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class TowerStatus(str, Enum):
    alive = 'alive'
    unreachable = 'unreachable'


class TowerBase(BaseModel):
    company: str
    hostname: str
    ipv4: str
    username: str
    port: int


class TowerRequest(TowerBase):
    password: str


class TowerResponse(TowerBase):
    id: int
    tower_status: TowerStatus
    created_at: datetime
    last_modified_at: datetime
    created_by: str
    last_modified_by: str

    class Config:
        orm_mode = True


class TowerRelationship(BaseModel):
    id: int
    company: str

    class Config:
        orm_mode = True
