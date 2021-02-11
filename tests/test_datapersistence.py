from unittest import TestCase
import datetime

from models.item import Item
from models.note import Note
from models.task import Task
from data.datapersistence import SqlitePersistence


class TestSqlitePersistence(TestCase):
    _item = Item()
    _note = Note()
    _task = Task()
    _db = SqlitePersistence(":memory:")


    def setUp(self):
        self._db.reset_session()
        self._db.truncate_all_tables()
        item = Item()
        note = Note()
        task = Task()

        self._item.rig = item.rig = "X01"
        self._item.description = item.description = "Something to handover"
        self._item.case = item.case = "CAS-12345"
        item_saved = self._db.save(item)

        self._note.description = note.description = "Some update"
        self._note.item_id = note.item_id = 1
        note_saved = self._db.save(note)

        self._task.description = task.description = "Some update"
        self._task.item_id = task.item_id = 1
        task_saved = self._db.save(task)

    def test_save(self):
        self._db.reset_session()
        self._db.truncate_all_tables()
        self._db.save(self._item)
        self._db.save(self._note)
        self._db.save(self._task)

        items = self._db.session.query(Item).all()

        item_count = len(items)
        note_count = len(self._db.session.query(Note).all())
        task_count = len(self._db.session.query(Task).all())

        self.assertEqual(1, item_count)
        self.assertEqual(1, note_count)
        self.assertEqual(1, task_count)




    def test_find(self):
        items = self._db.session.query(Item).all()
        print(items)
        item_found = self._db.find(Item, 1)
        note_found = self._db.find(Note, 1)
        task_found = self._db.find(Task, 1)

        self.assertEqual(self._item.description, item_found.description)
        self.assertEqual(self._note.description, note_found.description)
        self.assertEqual(self._task.description, task_found.description)

        self.assertRaises(Exception, self._db.find(Item, 50))



    def test_get_incomplete_items(self):
        item2 = Item()
        item2.rig = "X02"
        item2.description = "Another description"
        item2.case = "CAS-23456"
        self._db.save(item2)
        self._db.complete(Item, 2)

        incomplete_items = self._db.get_incomplete_items()

        self.assertEqual(1, len(incomplete_items))
        self.assertEqual(self._item.rig, incomplete_items[0].rig)


    def test_edit(self):
        item = self._db.find(Item, 1)

        data = {"rig": "X03",
                "description": "something else",
                "case": "123456"}
        self._db.edit(Item, item.id, data)
        edited = self._db.find(Item, 1)

        self.assertEqual(data["rig"], edited.rig)
        self.assertEqual(data["description"], edited.description)
        self.assertEqual(data["case"], edited.case)

        note = self._db.find(Note, 1)
        data = {"description": "another note"}
        self._db.edit(Note, note.id, data)
        edited = self._db.find(Note, note.id)

        self.assertEqual(data["description"], edited.description)

        task = self._db.find(Task, 1)
        self._db.edit(Task, task.id, data)
        edited = self._db.find(Task, task.id)

        self.assertEqual(data["description"], edited.description)

    def test_complete(self):
        item = self._db.find(Item, 1)
        self.assertIsNone(item.completed_at)

        self._db.complete(Item, item.id)

        completed_item = self._db.find(Item, 1)

        self.assertIsNotNone(completed_item.completed_at)

    def test_incomplete(self):
        item = self._db.find(Item, 1)
        self.assertIsNone(item.completed_at)
        self._db.complete(Item, item.id)
        completed_item = self._db.find(Item, 1)
        self.assertIsNotNone(completed_item.completed_at)
        self._db.incomplete(Item, completed_item.id)
        incomplete_item = self._db.find(Item, 1)
        self.assertIsNone(incomplete_item.completed_at)

    def test_get_items_completed_in_past_day(self):
        item2 = Item()
        item2.rig = "X02"
        item2.description = "Another description"
        item2.case = "CAS-23456"
        item2.completed_at = datetime.datetime.now() - datetime.timedelta(days=1)
        self._db.save(item2)
        self._db.complete(Item, 2)

        item1 = self._db.find(Item, 1)
        self._db.find(Item, item1.id)

        complete_items = self._db.get_items_completed_in_past_day()

        self.assertEqual(1, complete_items.count())

    def test_get_items_completed_in_past_day(self):
        item2 = Item()
        item2.rig = "X02"
        item2.description = "Another description"
        item2.case = "CAS-23456"
        item2.completed_at = datetime.datetime.now() - datetime.timedelta(days=6)
        self._db.save(item2)
        self._db.complete(Item, 2)

        item1 = self._db.find(Item, 1)
        self._db.find(Item, item1.id)

        complete_items = self._db.get_items_completed_in_past_day()

        self.assertEqual(1, complete_items.count())

    def prep_db(self):
        db = SqlitePersistence(":memory:")
        db.session.rollback()
        db.save(self._item)
        db.save(self._note)
        db.save(self._task)
        return db