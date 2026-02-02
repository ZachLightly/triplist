from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from ..db import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    items = relationship("Item", secondary="item_tags", back_populates="tags")
    