from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from ..database.connection import Base


class Project(Base):
    __tablename__ = "projects"

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
    source_control_credential_type = Column(
        'source_control_credential_type',
        Enum('manual', 'git', name='source_control_credential_type'),
        nullable=False
    )
    tool = Column(
        'tool',
        Enum('ansible', 'jenkins', 'terraform', 'playwright', name='tool'),
        nullable=False
    )
    project_status = Column(
        'project_status',
        Enum('pending', 'waiting', 'running', 'successful', 'failed', 'error',
             'canceled', 'never_updated', 'ok', 'missing', name='project_status'),
        nullable=False,
        server_default=text("'pending'")
    )
    source_control_url = Column(
        String,
        nullable=True
    )
    base_path = Column(
        String,
        nullable=True
    )
    playbook_directory = Column(
        String,
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
