from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..database.connection import Base


class Tower(Base):
    __tablename__ = "towers"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    company = Column(
        String,
        nullable=False,
        unique=True
    )
    hostname = Column(
        String,
        nullable=False
    )
    ipv4 = Column(
        String,
        nullable=False
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
    tower_status = Column(
        'tower_status',
        Enum('alive', 'unreachable', name='tower_status'),
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
