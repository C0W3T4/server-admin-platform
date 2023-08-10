from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class SortDir(str, Enum):
    asc = 'asc'
    desc = 'desc'


class JobsScheduleInfoBase(BaseModel):
    cron_job_id: str
    frequency: int
    frequency_per_hour: int
    frequency_per_day: int
    frequency_per_year: int
    prev_date: datetime
    next_date: datetime

    class Config:
        orm_mode = True
