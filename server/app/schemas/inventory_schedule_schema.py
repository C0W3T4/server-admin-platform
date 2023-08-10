from pydantic import BaseModel
from typing import List
from . import inventory_schema, schedule_schema


class InventoryScheduleBase(BaseModel):
    pass


class InventoryScheduleRequest(InventoryScheduleBase):
    inventory_id: int
    schedule_id: int


class InventorySchedulePostRequest(InventoryScheduleBase):
    schedules_id: List[int]
    inventory_id: int


class InventoryScheduleResponse(InventoryScheduleBase):
    inventory_schedule_id: int
    cron_job_id: str
    inventory: inventory_schema.InventoryResponse
    schedule: schedule_schema.ScheduleResponse

    class Config:
        orm_mode = True


class InventoriesScheduleResponse(InventoryScheduleBase):
    inventory_schedule_id: int
    cron_job_id: str
    inventory: inventory_schema.InventoryResponse

    class Config:
        orm_mode = True


class InventorySchedulesResponse(InventoryScheduleBase):
    inventory_schedule_id: int
    cron_job_id: str
    schedule: schedule_schema.ScheduleResponse

    class Config:
        orm_mode = True
