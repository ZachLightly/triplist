from sqlalchemy import Column, Integer, String, UUID, ForeignKey
from uuid import uuid4
from ..db import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(String, nullable=False)