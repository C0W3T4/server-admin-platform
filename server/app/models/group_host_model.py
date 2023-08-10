from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class GroupHost(Base):
    __tablename__ = "groups_hosts"

    group_host_id = Column(
        Integer,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            cycle=True
        )
    )
    group_id = Column(
        Integer,
        ForeignKey(
            "groups.id",
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

    group = relationship("Group")
    host = relationship("Host")
