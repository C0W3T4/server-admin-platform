from pydantic import BaseModel
from typing import List
from . import inventory_schema, group_schema


class InventoryGroupBase(BaseModel):
    pass


class InventoryGroupRequest(InventoryGroupBase):
    inventory_id: int
    group_id: int


class InventoryGroupPostRequest(InventoryGroupBase):
    groups_id: List[int]
    inventory_id: int


class InventoryGroupResponse(InventoryGroupBase):
    inventory_group_id: int
    inventory: inventory_schema.InventoryResponse
    group: group_schema.GroupResponse

    class Config:
        orm_mode = True


class InventoriesGroupResponse(InventoryGroupBase):
    inventory_group_id: int
    inventory: inventory_schema.InventoryResponse

    class Config:
        orm_mode = True


class InventoryGroupsResponse(InventoryGroupBase):
    inventory_group_id: int
    group: group_schema.GroupResponse

    class Config:
        orm_mode = True
