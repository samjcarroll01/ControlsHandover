from sqlalchemy import Column, Integer, Sequence, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    description = Column(String(255))
    created_by = Column(String(50))
    updated_by = Column(String(50))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    completed_at = Column(DateTime)
    item_id = Column(Integer, ForeignKey('items.id'))

    item = relationship("Item", back_populates="tasks")
