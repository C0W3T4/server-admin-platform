from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class UserHost(Base):
    __tablename__ = "users_hosts"

    user_host_id = Column(
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
    host_id = Column(
        Integer,
        ForeignKey(
            "hosts.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    user = relationship("User")
    host = relationship("Host")
