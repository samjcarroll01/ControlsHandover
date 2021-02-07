from sqlalchemy import Column, Integer, String, Sequence, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from models.note import Note
from models.task import Task


class Item(Base):
    """
    Model Class\n
    ---------------------------------------------\n
    Contains the following columns in the table:\n
    id - autoincrementing integer\n
    rig - String with max length of 50\n
    case - String with max length of 20\n
    description - String with max length of 255\n
    created_by - String with max length of 50\n
    updated_by - String with max length of 50\n
    created_at - Timestamp\n
    updated_at - Timestamp\n
    completed_at - Timestamp\n
    --------------------------------------------\n
    Has the following relationships:\n
    notes - List of notes associated with the item\n
    tasks - List of tasks associated with the item\n
    """

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
