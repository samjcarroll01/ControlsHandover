import configparser
import random
from models.item import Item
from viewmodels.itemlist import ItemList
from data.datapersistence import SqlitePersistence

config = configparser.ConfigParser()
config.read("config.ini")
db = SqlitePersistence(config.get("Database", "path"))

db.truncate_all_tables()

for i in range(1, 31):
    item = Item()
    item.rig = "X0%i" % i
    item.description = "Something that needs to be handed over"
    item.case = "CAS-12345"

    db.save(item)

for i in range(1, 31):
    rand = random.random()
    if rand * i / 30 > 0.1:
        db.complete(Item, i)

itemList = ItemList()

db_item = db.find(Item, 1)

print("\nOpen items (%i)" % len(itemList.open))
for i in range(0, len(itemList.open)):
    print(itemList.open[i].id, itemList.open[i].rig, "-", itemList.open[i].description)

print("\nItems closed in the last day (%i):" % len(itemList.closed_in_last_day))
for i in range(0, len(itemList.closed_in_last_day)):
    print(itemList.closed_in_last_day[i].id, itemList.closed_in_last_day[i].rig, "-", itemList.closed_in_last_day[i].description)
