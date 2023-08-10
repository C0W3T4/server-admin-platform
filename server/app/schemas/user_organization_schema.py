from pydantic import BaseModel
from typing import List
from . import user_schema, organization_schema


class UserOrganizationBase(BaseModel):
    pass


class UserOrganizationRequest(UserOrganizationBase):
    user_id: int
    organization_id: int


class UserOrganizationPostRequest(UserOrganizationBase):
    users_id: List[int]
    organization_id: int


class UserOrganizationResponse(UserOrganizationBase):
    user_organization_id: int
    user: user_schema.UserResponse
    organization: organization_schema.OrganizationResponse

    class Config:
        orm_mode = True


class UsersOrganizationResponse(UserOrganizationBase):
    user_organization_id: int
    user: user_schema.UserResponse

    class Config:
        orm_mode = True


class UserOrganizationsResponse(UserOrganizationBase):
    user_organization_id: int
    organization: organization_schema.OrganizationResponse

    class Config:
        orm_mode = True
