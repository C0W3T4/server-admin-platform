from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class InventoryGroup(Base):
    __tablename__ = "inventories_groups"

    inventory_group_id = Column(
        Integer,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            cycle=True
        )
    )
    inventory_id = Column(
        Integer,
        ForeignKey(
            "inventories.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    group_id = Column(
        Integer,
        ForeignKey(
            "groups.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    inventory = relationship("Inventory")
    group = relationship("Group")
