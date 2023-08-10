from typing import List, Optional
from pydantic import BaseModel
from app.schemas import user_schema, tower_schema, organization_schema, team_schema


class RegisterAccountRequest(BaseModel):
    company: str
    hostname: str
    ipv4: str
    username: str
    port: int
    password: str
    admin_username: str
    admin_password: str
    organization_name: str


class RegisterAccountResponse(BaseModel):
    tower: tower_schema.TowerResponse
    user: user_schema.UserResponse
    organization: organization_schema.OrganizationResponse


class UserLoginBase(BaseModel):
    username: str


class UserLoginRequest(UserLoginBase):
    password: str


class TokenBase(BaseModel):
    pass


class TokenData(TokenBase):
    user_id: Optional[str] = None


class TokenResponse(TokenBase):
    user: user_schema.UserResponse
    teams: Optional[List[team_schema.TeamRelationship]]
    organizations: Optional[List[organization_schema.OrganizationRelationship]]
    access_token: str
    token_type: str
