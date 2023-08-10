from pydantic import BaseModel
from typing import List
from . import template_schema, user_schema


class UserTemplateBase(BaseModel):
    pass


class UserTemplateRequest(UserTemplateBase):
    user_id: int
    template_id: int


class UserTemplatePostRequest(UserTemplateBase):
    users_id: List[int]
    template_id: int


class UserTemplateResponse(UserTemplateBase):
    user_template_id: int
    user: user_schema.UserResponse
    template: template_schema.TemplateResponse

    class Config:
        orm_mode = True


class UsersTemplateResponse(UserTemplateBase):
    user_template_id: int
    user: user_schema.UserResponse

    class Config:
        orm_mode = True


class UserTemplatesResponse(UserTemplateBase):
    user_template_id: int
    template: template_schema.TemplateResponse

    class Config:
        orm_mode = True
