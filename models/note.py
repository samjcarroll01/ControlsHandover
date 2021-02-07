from sqlalchemy import Column, Integer, Sequence, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base


class Note(Base):
    """
        Model Class\n
        ---------------------------------------------\n
        Contains the following columns in the table:\n
        id - autoincrementing Integer\n
        description - String with max length of 255\n
        created_by - String with max length of 50\n
        updated_by - String with max length of 50\n
        created_at - Timestamp\n
        updated_at - Timestamp\n
        item_id - Integer\n
        --------------------------------------------\n
        Has the following relationships:\n
        item - the item this note is associated with\n
        """

    __tablename__ = "notes"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    description = Column(String(255))
    created_by = Column(String(50))
    updated_by = Column(String(50))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    item_id = Column(Integer, ForeignKey('items.id'))

    item = relationship("Item", back_populates="notes")
