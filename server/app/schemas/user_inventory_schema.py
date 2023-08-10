from pydantic import BaseModel
from typing import List
from . import inventory_schema, user_schema


class UserInventoryBase(BaseModel):
    pass


class UserInventoryRequest(UserInventoryBase):
    user_id: int
    inventory_id: int


class UserInventoryPostRequest(UserInventoryBase):
    users_id: List[int]
    inventory_id: int


class UserInventoryResponse(UserInventoryBase):
    user_inventory_id: int
    user: user_schema.UserResponse
    inventory: inventory_schema.InventoryResponse

    class Config:
        orm_mode = True


class UsersInventoryResponse(UserInventoryBase):
    user_inventory_id: int
    user: user_schema.UserResponse

    class Config:
        orm_mode = True


class UserInventoriesResponse(UserInventoryBase):
    user_inventory_id: int
    inventory: inventory_schema.InventoryResponse

    class Config:
        orm_mode = True
