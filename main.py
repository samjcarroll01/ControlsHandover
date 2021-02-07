import datetime
import os

from models.item import Item
from data.datapersistence import SqlitePersistence

db = SqlitePersistence(":memory:")

item = Item()
item.rig = "X04"
item.description = "Something that needs to be handed over"
item.created_at = datetime.datetime.now()
item.updated_at = item.created_at
item.created_by = os.getlogin()
item.updated_by = os.getlogin()
item.case = "CAS-12345"

db.save(item)

db_item = db.find(Item, 1)

print(db_item.rig)
print(db_item.created_by)


