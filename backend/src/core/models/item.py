from sqlalchemy import Column, Integer, String, UUID, ForeignKey, Table
from sqlalchemy.orm import relationship
from uuid import uuid4
from ..db import Base

# Many-to-many association table
item_tags = Table(
    'item_tags',
    Base.metadata,
    Column('item_id', UUID, ForeignKey('items.id')),
    Column('tag_id', UUID, ForeignKey('tags.id'))
)

class Item(Base):
    __tablename__ = "items"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    name = Column(String, nullable=False)
    tags = relationship("Tag", secondary=item_tags, back_populates="items")
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)