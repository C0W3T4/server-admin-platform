from pydantic import BaseModel
from typing import List
from app.schemas import template_schema, schedule_schema


class TemplateScheduleBase(BaseModel):
    pass


class TemplateScheduleRequest(TemplateScheduleBase):
    template_id: int
    schedule_id: int


class TemplateSchedulePostRequest(TemplateScheduleBase):
    schedules_id: List[int]
    template_id: int


class TemplateScheduleResponse(TemplateScheduleBase):
    template_schedule_id: int
    cron_job_id: str
    template: template_schema.TemplateResponse
    schedule: schedule_schema.ScheduleResponse

    class Config:
        orm_mode = True


class TemplatesScheduleResponse(TemplateScheduleBase):
    template_schedule_id: int
    cron_job_id: str
    template: template_schema.TemplateResponse

    class Config:
        orm_mode = True


class TemplateSchedulesResponse(TemplateScheduleBase):
    template_schedule_id: int
    cron_job_id: str
    schedule: schedule_schema.ScheduleResponse

    class Config:
        orm_mode = True
