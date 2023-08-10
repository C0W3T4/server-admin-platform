from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class TeamHost(Base):
    __tablename__ = "teams_hosts"

    team_host_id = Column(
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
    host_id = Column(
        Integer,
        ForeignKey(
            "hosts.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    team = relationship("Team")
    host = relationship("Host")
