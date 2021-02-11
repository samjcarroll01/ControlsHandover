import configparser
from data.datapersistence import SqlitePersistence


class ItemList:
    _db = None
    open = []
    closed_in_last_day = []
    closed_in_last_week = []

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self._db = SqlitePersistence(config.get("Database", "path"))
        self.open = self._db.get_incomplete_items()
        self.closed_in_last_day = self._db.get_items_completed_in_past_day()
        self.closed_in_last_week = self._db.get_items_completed_in_past_week()
