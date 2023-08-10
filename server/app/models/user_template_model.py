from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class UserTemplate(Base):
    __tablename__ = "users_templates"

    user_template_id = Column(
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
    template_id = Column(
        Integer,
        ForeignKey(
            "templates.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    user = relationship("User")
    template = relationship("Template")
