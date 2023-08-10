from sqlalchemy import Column, Identity, Integer, ForeignKey, String
from ..database.connection import Base
from sqlalchemy.orm import relationship


class InventorySchedule(Base):
    __tablename__ = "inventories_schedules"

    inventory_schedule_id = Column(
        Integer,
        Identity(
            start=1,
            increment=1,
            minvalue=1,
            cycle=True
        )
    )
    cron_job_id = Column(
        String,
        nullable=False,
        unique=True
    )
    inventory_id = Column(
        Integer,
        ForeignKey(
            "inventories.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    schedule_id = Column(
        Integer,
        ForeignKey(
            "schedules.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    inventory = relationship("Inventory")
    schedule = relationship("Schedule")
