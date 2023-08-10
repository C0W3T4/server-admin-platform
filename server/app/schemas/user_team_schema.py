from pydantic import BaseModel
from typing import List
from . import user_schema, team_schema


class UserTeamBase(BaseModel):
    pass


class UserTeamRequest(UserTeamBase):
    user_id: int
    team_id: int


class UserTeamPostRequest(UserTeamBase):
    users_id: List[int]
    team_id: int


class UserTeamResponse(UserTeamBase):
    user_team_id: int
    user: user_schema.UserResponse
    team: team_schema.TeamResponse

    class Config:
        orm_mode = True


class UsersTeamResponse(UserTeamBase):
    user_team_id: int
    user: user_schema.UserResponse

    class Config:
        orm_mode = True


class UserTeamsResponse(UserTeamBase):
    user_team_id: int
    team: team_schema.TeamResponse

    class Config:
        orm_mode = True
