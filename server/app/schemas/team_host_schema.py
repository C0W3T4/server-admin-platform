from pydantic import BaseModel
from typing import List
from . import host_schema, team_schema


class TeamHostBase(BaseModel):
    pass


class TeamHostRequest(TeamHostBase):
    team_id: int
    host_id: int


class TeamHostPostRequest(TeamHostBase):
    teams_id: List[int]
    host_id: int


class TeamHostResponse(TeamHostBase):
    team_host_id: int
    team: team_schema.TeamResponse
    host: host_schema.HostResponse

    class Config:
        orm_mode = True


class TeamsHostResponse(TeamHostBase):
    team_host_id: int
    team: team_schema.TeamResponse

    class Config:
        orm_mode = True
