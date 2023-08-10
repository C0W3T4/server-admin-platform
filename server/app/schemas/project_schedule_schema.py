from pydantic import BaseModel
from typing import List
from app.schemas import project_schema, schedule_schema


class ProjectScheduleBase(BaseModel):
    pass


class ProjectScheduleRequest(ProjectScheduleBase):
    project_id: int
    schedule_id: int


class ProjectSchedulePostRequest(ProjectScheduleBase):
    schedules_id: List[int]
    project_id: int


class ProjectScheduleResponse(ProjectScheduleBase):
    project_schedule_id: int
    cron_job_id: str
    project: project_schema.ProjectResponse
    schedule: schedule_schema.ScheduleResponse

    class Config:
        orm_mode = True


class ProjectsScheduleResponse(ProjectScheduleBase):
    project_schedule_id: int
    cron_job_id: str
    project: project_schema.ProjectResponse

    class Config:
        orm_mode = True


class ProjectSchedulesResponse(ProjectScheduleBase):
    project_schedule_id: int
    cron_job_id: str
    schedule: schedule_schema.ScheduleResponse

    class Config:
        orm_mode = True
