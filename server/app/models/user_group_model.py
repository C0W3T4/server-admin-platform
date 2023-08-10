from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class UserGroup(Base):
    __tablename__ = "users_groups"

    user_group_id = Column(
        Integer,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            cycle=True
        )
    )
    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    group_id = Column(
        Integer,
        ForeignKey(
            "groups.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    user = relationship("User")
    group = relationship("Group")
