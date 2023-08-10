from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from ..database.connection import Base


class Host(Base):
    __tablename__ = "hosts"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    description = Column(
        String,
        nullable=True
    )
    hostname = Column(
        String,
        nullable=False
    )
    ipv4 = Column(
        String,
        nullable=False
    )
    host_status = Column(
        'host_status',
        Enum('alive', 'successful', 'failed',
             'unreachable', name='host_status'),
        nullable=False,
        server_default=text("'alive'")
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
    last_modified_by = Column(
        String,
        nullable=False
    )
    created_by = Column(
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
