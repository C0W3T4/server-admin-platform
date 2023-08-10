from pydantic import BaseModel
from typing import List
from . import group_schema, team_schema


class TeamGroupBase(BaseModel):
    pass


class TeamGroupRequest(TeamGroupBase):
    team_id: int
    group_id: int


class TeamGroupPostRequest(TeamGroupBase):
    teams_id: List[int]
    group_id: int


class TeamGroupResponse(TeamGroupBase):
    team_group_id: int
    team: team_schema.TeamResponse
    group: group_schema.GroupResponse

    class Config:
        orm_mode = True


class TeamsGroupResponse(TeamGroupBase):
    team_group_id: int
    team: team_schema.TeamResponse

    class Config:
        orm_mode = True
