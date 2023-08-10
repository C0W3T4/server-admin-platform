from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..database.connection import Base
from sqlalchemy.orm import relationship


class Template(Base):
    __tablename__ = "templates"

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
    launch_type = Column(
        'launch_type',
        Enum('run', 'check', name='launch_type'),
        nullable=False,
        server_default=text("'run'")
    )
    playbook_name = Column(
        String,
        nullable=False
    )
    limit = Column(
        String,
        nullable=True
    )
    privilege_escalation = Column(
        Boolean,
        nullable=False,
        server_default='FALSE'
    )
    verbosity = Column(
        'verbosity',
        Enum('0', 'v', 'vv', 'vvv', 'vvvv',
             'vvvvv', 'vvvvvv', name='verbosity'),
        nullable=False,
        server_default=text("'0'")
    )
    forks = Column(
        Integer,
        nullable=False,
        server_default=text('5')
    )
    extra_vars = Column(
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
    inventory_id = Column(
        Integer,
        ForeignKey(
            "inventories.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    credential_id = Column(
        Integer,
        ForeignKey(
            "credentials.id",
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

    inventory = relationship("Inventory")
    project = relationship("Project")
    credential = relationship("Credential")
    organization = relationship("Organization")
