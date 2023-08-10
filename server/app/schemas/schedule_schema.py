from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List, Optional
from . import organization_schema


class ScheduleType(str, Enum):
    template = 'template'
    project = 'project'
    inventory = 'inventory'


class ScheduleRepeatFrequency(str, Enum):
    run_once = 'run_once'
    minute = 'minute'
    hour = 'hour'
    day = 'day'
    week = 'week'
    month = 'month'
    year = 'year'


class ScheduleWeekdays(str, Enum):
    sun = 'sun'
    mon = 'mon'
    tue = 'tue'
    wed = 'wed'
    thu = 'thu'
    fri = 'fri'
    sat = 'sat'


class ScheduleBase(BaseModel):
    name: str
    description: Optional[str]
    start_date_time: datetime
    repeat_frequency: ScheduleRepeatFrequency
    every: Optional[int]
    week_days: Optional[List[int]]


class ScheduleRequest(ScheduleBase):
    schedule_type: ScheduleType
    organization_id: int


class ScheduleUpdateRequest(ScheduleBase):
    organization_id: int


class ScheduleResponse(ScheduleBase):
    id: int
    schedule_type: ScheduleType
    created_at: datetime
    last_modified_at: datetime
    created_by: str
    last_modified_by: str
    organization: organization_schema.OrganizationRelationship

    class Config:
        orm_mode = True


class ScheduleRelationship(BaseModel):
    id: int
    name: str
    schedule_type: ScheduleType

    class Config:
        orm_mode = True
