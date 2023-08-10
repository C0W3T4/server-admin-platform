from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class UserProject(Base):
    __tablename__ = "users_projects"

    user_project_id = Column(
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
    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    user = relationship("User")
    project = relationship("Project")
