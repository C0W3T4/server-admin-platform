from pydantic import BaseModel


class DashboardBase(BaseModel):
    pass


class DashboardRequest(DashboardBase):
    pass


class DashboardResponse(DashboardBase):
    pass

    class Config:
        orm_mode = True


class DashboardTotalsResponse(DashboardBase):
    total_users: int
    total_teams: int
    total_organizations: int
    total_credentials: int
    total_inventories: int
    total_groups: int
    total_hosts: int
    total_projects: int
    total_templates: int
    total_schedules: int
    total_jobs: int

    class Config:
        orm_mode = True
