from pydantic import BaseModel
from typing import List
from . import team_schema, organization_schema


class TeamOrganizationBase(BaseModel):
    pass


class TeamOrganizationRequest(TeamOrganizationBase):
    team_id: int
    organization_id: int


class TeamOrganizationPostRequest(TeamOrganizationBase):
    teams_id: List[int]
    organization_id: int


class TeamOrganizationResponse(TeamOrganizationBase):
    team_organization_id: int
    team: team_schema.TeamResponse
    organization: organization_schema.OrganizationResponse

    class Config:
        orm_mode = True


class TeamsOrganizationResponse(TeamOrganizationBase):
    team_organization_id: int
    team: team_schema.TeamResponse

    class Config:
        orm_mode = True
