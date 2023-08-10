from pydantic import BaseModel
from typing import List
from . import template_schema, team_schema


class TeamTemplateBase(BaseModel):
    pass


class TeamTemplateRequest(TeamTemplateBase):
    team_id: int
    template_id: int


class TeamTemplatePostRequest(TeamTemplateBase):
    teams_id: List[int]
    template_id: int


class TeamTemplateResponse(TeamTemplateBase):
    team_template_id: int
    team: team_schema.TeamResponse
    template: template_schema.TemplateResponse

    class Config:
        orm_mode = True


class TeamsTemplateResponse(TeamTemplateBase):
    team_template_id: int
    team: team_schema.TeamResponse

    class Config:
        orm_mode = True
