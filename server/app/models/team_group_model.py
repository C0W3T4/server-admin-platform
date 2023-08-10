from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class TeamGroup(Base):
    __tablename__ = "teams_groups"

    team_group_id = Column(
        Integer,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            cycle=True
        )
    )
    team_id = Column(
        Integer,
        ForeignKey(
            "teams.id",
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

    team = relationship("Team")
    group = relationship("Group")
