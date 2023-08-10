from pydantic import BaseModel
from typing import List
from . import credential_schema, team_schema


class TeamCredentialBase(BaseModel):
    pass


class TeamCredentialRequest(TeamCredentialBase):
    team_id: int
    credential_id: int


class TeamCredentialPostRequest(TeamCredentialBase):
    teams_id: List[int]
    credential_id: int


class TeamCredentialResponse(TeamCredentialBase):
    team_credential_id: int
    team: team_schema.TeamResponse
    credential: credential_schema.CredentialResponse

    class Config:
        orm_mode = True


class TeamsCredentialResponse(TeamCredentialBase):
    team_credential_id: int
    team: team_schema.TeamResponse

    class Config:
        orm_mode = True
