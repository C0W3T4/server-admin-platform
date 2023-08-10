from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class UserInventory(Base):
    __tablename__ = "users_inventories"

    user_inventory_id = Column(
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
    inventory_id = Column(
        Integer,
        ForeignKey(
            "inventories.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    user = relationship("User")
    inventory = relationship("Inventory")
