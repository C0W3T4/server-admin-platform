from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional
from app.schemas import organization_schema


class InventoryStatus(str, Enum):
    successful = 'successful'
    disabled = 'disabled'
    error = 'error'


class InventoryBase(BaseModel):
    name: str
    description: Optional[str]
    inventory_file: str


class InventoryRequest(InventoryBase):
    organization_id: int


class InventoryResponse(InventoryBase):
    id: int
    inventory_status: InventoryStatus
    created_at: datetime
    last_modified_at: datetime
    created_by: str
    last_modified_by: str
    organization: organization_schema.OrganizationRelationship

    class Config:
        orm_mode = True


class InventoryRelationship(BaseModel):
    id: int
    name: str
    inventory_status: InventoryStatus

    class Config:
        orm_mode = True
