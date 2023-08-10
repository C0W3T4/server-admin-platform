from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class UserOrganization(Base):
    __tablename__ = "users_organizations"

    user_organization_id = Column(
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
    organization_id = Column(
        Integer,
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    user = relationship("User")
    organization = relationship("Organization")
