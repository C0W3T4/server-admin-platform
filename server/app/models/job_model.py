from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from ..database.connection import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    job_status = Column(
        'job_status',
        Enum('pending', 'waiting', 'running',
             'successful', 'failed', name='job_status'),
        nullable=False,
        server_default=text("'pending'")
    )
    started_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False
    )
    finished_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False
    )
    launched_by = Column(
        String,
        nullable=False
    )
    output = Column(
        String,
        nullable=False
    )
    template_id = Column(
        Integer,
        ForeignKey(
            "templates.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    organization_id = Column(
        Integer,
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    template = relationship("Template")
    organization = relationship("Organization")
