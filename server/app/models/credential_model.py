from sqlalchemy import Column, Enum, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from ..database.connection import Base


class Credential(Base):
    __tablename__ = "credentials"

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
    username = Column(
        String,
        nullable=False
    )
    password = Column(
        String,
        nullable=False
    )
    port = Column(
        Integer,
        nullable=False
    )
    credential_type = Column(
        'credential_type',
        Enum('machine', 'source_control', name='credential_type'),
        nullable=False
    )
    ssh_key = Column(
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
