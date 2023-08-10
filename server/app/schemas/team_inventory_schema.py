from pydantic import BaseModel
from typing import List
from . import inventory_schema, team_schema


class TeamInventoryBase(BaseModel):
    pass


class TeamInventoryRequest(TeamInventoryBase):
    team_id: int
    inventory_id: int


class TeamInventoryPostRequest(TeamInventoryBase):
    teams_id: List[int]
    inventory_id: int


class TeamInventoryResponse(TeamInventoryBase):
    team_inventory_id: int
    team: team_schema.TeamResponse
    inventory: inventory_schema.InventoryResponse

    class Config:
        orm_mode = True


class TeamsInventoryResponse(TeamInventoryBase):
    team_inventory_id: int
    team: team_schema.TeamResponse

    class Config:
        orm_mode = True
