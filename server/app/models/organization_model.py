from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..database.connection import Base
from sqlalchemy.orm import relationship


class Organization(Base):
    __tablename__ = "organizations"

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
    tower_id = Column(
        Integer,
        ForeignKey(
            "towers.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    tower = relationship("Tower")
