from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class TeamTemplate(Base):
    __tablename__ = "teams_templates"

    team_template_id = Column(
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
    template_id = Column(
        Integer,
        ForeignKey(
            "templates.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    team = relationship("Team")
    template = relationship("Template")
