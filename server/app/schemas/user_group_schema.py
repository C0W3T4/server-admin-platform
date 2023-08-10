from pydantic import BaseModel
from typing import List
from . import group_schema, user_schema


class UserGroupBase(BaseModel):
    pass


class UserGroupRequest(UserGroupBase):
    user_id: int
    group_id: int


class UserGroupPostRequest(UserGroupBase):
    users_id: List[int]
    group_id: int


class UserGroupResponse(UserGroupBase):
    user_group_id: int
    user: user_schema.UserResponse
    group: group_schema.GroupResponse

    class Config:
        orm_mode = True


class UsersGroupResponse(UserGroupBase):
    user_group_id: int
    user: user_schema.UserResponse

    class Config:
        orm_mode = True


class UserGroupsResponse(UserGroupBase):
    user_group_id: int
    group: group_schema.GroupResponse

    class Config:
        orm_mode = True
