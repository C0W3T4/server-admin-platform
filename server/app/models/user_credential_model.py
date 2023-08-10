from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class UserCredential(Base):
    __tablename__ = "users_credentials"

    user_credential_id = Column(
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
    credential_id = Column(
        Integer,
        ForeignKey(
            "credentials.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    user = relationship("User")
    credential = relationship("Credential")
