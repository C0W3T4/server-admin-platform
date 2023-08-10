from sqlalchemy import Column, Identity, Integer, ForeignKey, String
from ..database.connection import Base
from sqlalchemy.orm import relationship


class TemplateSchedule(Base):
    __tablename__ = "templates_schedules"

    template_schedule_id = Column(
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
    template_id = Column(
        Integer,
        ForeignKey(
            "templates.id",
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

    template = relationship("Template")
    schedule = relationship("Schedule")
