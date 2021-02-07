from unittest import TestCase
from models.item import Item
from models.note import Note
from models.task import Task
from data.datapersistence import SqlitePersistence
import os


class TestItem(TestCase):
    _item = Item()
    _note = Note()
    _task = Task()
    _db = SqlitePersistence(":memory:")

    def setUp(self):
        self._item.rig = "X01"
        self._item.description = "Something to handover"
        self._item.case = "CAS-12345"
        self._db.save(self._item)

        self._note.description = "Some update"
        self._note.item_id = 1
        self._db.save(self._note)

        self._task.description = "Some update"
        self._task.item_id = 1
        self._db.save(self._task)

    def test_an_item_has_a_rig(self):
        self.assertEqual(self._item.rig, "X01")

    def test_an_item_has_a_description(self):
        self.assertEqual(self._item.description, "Something to handover")

    def test_an_item_has_a_case(self):
        self.assertEqual(self._item.case, "CAS-12345")

    def test_a_saved_item_has_a_created_at_timestamp(self):
        item = self._db.find(Item, 1)
        self.assertIsNotNone(item.created_at)

    def test_a_saved_item_has_an_updated_at_timestamp(self):
        item = self._db.find(Item, 1)
        self.assertIsNotNone(item.updated_at)

    def test_a_saved_item_has_a_created_by(self):
        item = self._db.find(Item, 1)
        self.assertEqual(item.created_by, os.getlogin())

    def test_a_saved_item_that_is_not_complete_does_not_have_a_completed_at_timestamp(self):
        item = self._db.find(Item, 1)
        self._db.incomplete(Item, item.id)

        item = self._db.find(Item, item.id)

        self.assertIsNone(item.completed_at)

    def test_a_saved_item_that_is_completed_has_a_completed_at_timestamp(self):
        item = self._db.find(Item, 1)
        self._db.complete(Item, item.id);

        item = self._db.find(Item, item.id)
        self.assertIsNotNone(item.completed_at)
        self.assertEqual(item.updated_at, item.completed_at)
        self.assertEqual(item.updated_by, os.getlogin())

    def test_an_item_has_notes(self):
        note = self._db.find(Note, 1)
        item = self._db.find(Item, 1)

        self.assertEqual(item.notes[0].description, note.description)

    def test_an_item_has_tasks(self):
        task = self._db.find(Task, 1)
        item = self._db.find(Item, 1)

        self.assertEqual(item.tasks[0].description, task.description)