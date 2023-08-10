from pydantic import BaseModel
from typing import List
from . import project_schema, team_schema


class TeamProjectBase(BaseModel):
    pass


class TeamProjectRequest(TeamProjectBase):
    team_id: int
    project_id: int


class TeamProjectPostRequest(TeamProjectBase):
    teams_id: List[int]
    project_id: int


class TeamProjectResponse(TeamProjectBase):
    team_project_id: int
    team: team_schema.TeamResponse
    project: project_schema.ProjectResponse

    class Config:
        orm_mode = True


class TeamsProjectResponse(TeamProjectBase):
    team_project_id: int
    team: team_schema.TeamResponse

    class Config:
        orm_mode = True
