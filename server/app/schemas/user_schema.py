from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import List, Optional
from . import team_schema, organization_schema, tower_schema


class UserType(str, Enum):
    normal_user = 'normal_user'
    system_auditor = 'system_auditor'
    system_administrator = 'system_administrator'
    admin = 'admin'


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    username: str
    roles: Optional[List[str]]
    user_type: UserType


class UserRequest(UserBase):
    password: str


class CurrentUserRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    username: str
    # password: Optional[str]


class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_modified_at: datetime
    created_by: str
    last_modified_by: str
    tower: tower_schema.TowerRelationship

    class Config:
        orm_mode = True


class CurrentUserResponse(BaseModel):
    user: UserResponse
    teams: Optional[List[team_schema.TeamRelationship]]
    organizations: Optional[List[organization_schema.OrganizationRelationship]]


class UserRelationship(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
