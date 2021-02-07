from sqlalchemy import Column, Integer, String, Sequence, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from models.note import Note
from models.task import Task


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    rig = Column(String(50), nullable=True)
    case = Column(String(20), nullable=True)
    description = Column(String(255))
    created_by = Column(String(50))
    updated_by = Column(String(50))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    completed_at = Column(DateTime)
    notes = relationship("Note", order_by=Note.created_at, back_populates="item")
    tasks = relationship("Task", order_by=Task.created_at, back_populates="item")

    def __init__(self):
        Base.__init__(self)