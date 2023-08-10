from sqlalchemy import Column, Integer, String, Enum, ARRAY, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..database.connection import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    first_name = Column(
        String,
        nullable=True
    )
    last_name = Column(
        String,
        nullable=True
    )
    email = Column(
        String,
        nullable=True,
        unique=True
    )
    username = Column(
        String,
        nullable=False
    )
    password = Column(
        String,
        nullable=False
    )
    roles = Column(
        ARRAY(String),
        nullable=True
    )
    user_type = Column(
        'user_type',
        Enum('normal_user', 'system_auditor',
             'system_administrator', 'admin', name='user_type'),
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
        server_default=text('now()')
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
