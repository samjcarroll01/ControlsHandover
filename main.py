import configparser
import random
from models.item import Item
from viewmodels.itemlist import ItemList
from data.datapersistence import SqlitePersistence


def main():
    setup()
    item_list = ItemList()
    print_items(item_list)


def setup():
    # Setup database connection
    config = configparser.ConfigParser()
    config.read("config.ini")
    db = SqlitePersistence(config.get("Database", "path"))

    # truncate all tables from previous run.
    # DO NOT INCLUDE IN PRODUCTION CODE, otherwise you will overwrite your data each time the program is started.
    db.truncate_all_tables()

    # Seed the database with items.
    for i in range(1, 31):
        item = Item()
        item.rig = "X0%i" % i
        item.description = "Something that needs to be handed over"
        item.case = "CAS-12345"

        db.save(item)

    # Complete random items.
    for i in range(1, 31):
        rand = random.random()
        # Items with lower ids are more likely to be completed than items with higher ids.
        if (rand * 2) + ((31 - i) / 30) > 1:
            db.complete(Item, i)


def print_items(item_list):
    # Print the open items
    print("\nOpen items (%i)" % len(item_list.open))
    print_item_list(item_list.open)

    # Print the items closed in the past day.
    print("\nItems closed in the last day (%i):" % len(item_list.closed_in_last_day))
    print_item_list(item_list.closed_in_last_day)


def print_item_list(item_list):
    for i in range(0, len(item_list)):
        print(item_list[i].id, "\t", item_list[i].rig, "\t", item_list[i].description)


if __name__ == "__main__":
    main()
