from sqlalchemy import Column, Enum, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from ..database.connection import Base


class Inventory(Base):
    __tablename__ = "inventories"

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
    inventory_status = Column(
        'inventory_status',
        Enum('successful', 'disabled', 'error', name='inventory_status'),
        nullable=False,
        server_default=text("'disabled'")
    )
    inventory_file = Column(
        String,
        nullable=False
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
