from pydantic import BaseModel
from typing import List
from . import project_schema, user_schema


class UserProjectBase(BaseModel):
    pass


class UserProjectRequest(UserProjectBase):
    user_id: int
    project_id: int


class UserProjectPostRequest(UserProjectBase):
    users_id: List[int]
    project_id: int


class UserProjectResponse(UserProjectBase):
    user_project_id: int
    user: user_schema.UserResponse
    project: project_schema.ProjectResponse

    class Config:
        orm_mode = True


class UsersProjectResponse(UserProjectBase):
    user_project_id: int
    user: user_schema.UserResponse

    class Config:
        orm_mode = True


class UserProjectsResponse(UserProjectBase):
    user_project_id: int
    project: project_schema.ProjectResponse

    class Config:
        orm_mode = True
