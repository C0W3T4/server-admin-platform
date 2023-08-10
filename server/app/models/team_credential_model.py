from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class TeamCredential(Base):
    __tablename__ = "teams_credentials"

    team_credential_id = Column(
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
    credential_id = Column(
        Integer,
        ForeignKey(
            "credentials.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    team = relationship("Team")
    credential = relationship("Credential")
