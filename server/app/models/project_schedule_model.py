from sqlalchemy import Column, Identity, Integer, ForeignKey, String
from ..database.connection import Base
from sqlalchemy.orm import relationship


class ProjectSchedule(Base):
    __tablename__ = "projects_schedules"

    project_schedule_id = Column(
        Integer,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            cycle=True
        )
    )
    cron_job_id = Column(
        String,
        nullable=False,
        unique=True
    )
    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    schedule_id = Column(
        Integer,
        ForeignKey(
            "schedules.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    project = relationship("Project")
    schedule = relationship("Schedule")
