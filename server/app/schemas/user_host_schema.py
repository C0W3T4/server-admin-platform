from pydantic import BaseModel
from typing import List
from . import host_schema, user_schema


class UserHostBase(BaseModel):
    pass


class UserHostRequest(UserHostBase):
    user_id: int
    host_id: int


class UserHostPostRequest(UserHostBase):
    users_id: List[int]
    host_id: int


class UserHostResponse(UserHostBase):
    user_host_id: int
    user: user_schema.UserResponse
    host: host_schema.HostResponse

    class Config:
        orm_mode = True


class UsersHostResponse(UserHostBase):
    user_host_id: int
    user: user_schema.UserResponse

    class Config:
        orm_mode = True


class UserHostsResponse(UserHostBase):
    user_host_id: int
    host: host_schema.HostResponse

    class Config:
        orm_mode = True
