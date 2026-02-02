from sqlalchemy import Column, Integer, String, UUID, ForeignKey, Boolean
from uuid import uuid4
from ..db import Base

class TripItem(Base):
    __tablename__ = "trip_items"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    trip_id = Column(UUID, ForeignKey("trips.id"), nullable=False)
    item_id = Column(UUID, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, nullable=True, default=1)
    checked = Column(Boolean, nullable=False, default=False)