from sqlalchemy import ARRAY, Column, Enum, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from ..database.connection import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    name = Column(
        String,
        nullable=False
    )
    description = Column(
        String,
        nullable=True
    )
    schedule_type = Column(
        'schedule_type',
        Enum('template', 'project', 'inventory', name='schedule_type'),
        nullable=False
    )
    start_date_time = Column(
        TIMESTAMP(timezone=True),
        nullable=False
    )
    repeat_frequency = Column(
        'repeat_frequency',
        Enum('run_once', 'minute', 'hour', 'day', 'week',
             'month', 'year', name='repeat_frequency'),
        nullable=False
    )
    every = Column(
        Integer,
        nullable=True
    )
    week_days = Column(
        ARRAY(Integer),
        nullable=True
    )
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    last_modified_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()'),
        onupdate=text('now()')
    )
    created_by = Column(
        String,
        nullable=False
    )
    last_modified_by = Column(
        String,
        nullable=False
    )
    organization_id = Column(
        Integer,
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE"
        )
    )

    organization = relationship("Organization")
