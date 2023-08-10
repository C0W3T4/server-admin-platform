from sqlalchemy import Column, Identity, Integer, ForeignKey
from ..database.connection import Base
from sqlalchemy.orm import relationship


class TeamInventory(Base):
    __tablename__ = "teams_inventories"

    team_inventory_id = Column(
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
    inventory_id = Column(
        Integer,
        ForeignKey(
            "inventories.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    team = relationship("Team")
    inventory = relationship("Inventory")
