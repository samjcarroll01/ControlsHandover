from sqlalchemy import Column, Integer, String, Sequence, DateTime
from sqlalchemy.orm import relationship
from base import Base
from note import Note
from task import Task


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    rig = Column(String(50), nullable=True)
    description = Column(String(255))
    created_by = Column(String(50))
    updated_by = Column(String(50))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    completed_at = Column(DateTime)
    notes = relationship("Note", order_by=Note.id, back_populates="notes")
    tasks = relationship("Task", order_by=Task.id, back_populates="tasks")