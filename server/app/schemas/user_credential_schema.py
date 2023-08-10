from pydantic import BaseModel
from typing import List
from . import credential_schema, user_schema


class UserCredentialBase(BaseModel):
    pass


class UserCredentialRequest(UserCredentialBase):
    user_id: int
    credential_id: int


class UserCredentialPostRequest(UserCredentialBase):
    users_id: List[int]
    credential_id: int


class UserCredentialResponse(UserCredentialBase):
    user_credential_id: int
    user: user_schema.UserResponse
    credential: credential_schema.CredentialResponse

    class Config:
        orm_mode = True


class UsersCredentialResponse(UserCredentialBase):
    user_credential_id: int
    user: user_schema.UserResponse

    class Config:
        orm_mode = True


class UserCredentialsResponse(UserCredentialBase):
    user_credential_id: int
    credential: credential_schema.CredentialResponse

    class Config:
        orm_mode = True
