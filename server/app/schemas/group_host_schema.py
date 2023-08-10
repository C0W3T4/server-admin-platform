from pydantic import BaseModel
from typing import List
from . import host_schema, group_schema


class GroupHostBase(BaseModel):
    pass


class GroupHostRequest(GroupHostBase):
    group_id: int
    host_id: int


class GroupHostPostRequest(GroupHostBase):
    hosts_id: List[int]
    group_id: int


class GroupHostResponse(GroupHostBase):
    group_host_id: int
    group: group_schema.GroupResponse
    host: host_schema.HostResponse

    class Config:
        orm_mode = True


class GroupsHostResponse(GroupHostBase):
    group_host_id: int
    group: group_schema.GroupResponse

    class Config:
        orm_mode = True


class GroupHostsResponse(GroupHostBase):
    group_host_id: int
    host: host_schema.HostResponse

    class Config:
        orm_mode = True
