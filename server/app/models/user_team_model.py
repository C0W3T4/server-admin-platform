from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class UserTeam(Base):
    __tablename__ = "users_teams"

    user_team_id = Column(
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
    team_id = Column(
        Integer,
        ForeignKey(
            "teams.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    user = relationship("User")
    team = relationship("Team")
