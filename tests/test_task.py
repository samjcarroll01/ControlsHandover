from unittest import TestCase
import os
from models.item import Item
from models.task import Task
from data.datapersistence import SqlitePersistence

class TestTask(TestCase):
    _item = Item()
    _task = Task()
    _db = SqlitePersistence(":memory:")

    def setUp(self):
        self._item.rig = "X01"
        self._item.description = "Something to handover"
        self._item.case = "CAS-12345"
        self._db.save(self._item)

        self._task.description = "Some update"
        self._task.item_id = 1
        self._db.save(self._task)

    def test_a_task_has_a_description(self):
        task = self._db.find(Task, 1)
        self.assertEqual(task.description, "Some update")

    def test_a_task_has_an_item(self):
        task = self._db.find(Task, 1)
        self.assertEqual(task.item.description, self._item.description)

    def test_a_saved_task_has_a_created_by_timestamp(self):
        task = self._db.find(Task, 1)
        self.assertIsNotNone(task.created_by)

    def test_a_saved_task_has_an_updated_by_timestamp(self):
        task = self._db.find(Task, 1)
        self.assertIsNotNone(task.updated_by)

    def test_a_saved_task_has_a_created_by(self):
        task = self._db.find(Task, 1)
        self.assertEqual(task.created_by, os.getlogin())

    def test_a_saved_task_has_an_updated_by(self):
        task = self._db.find(Task, 1)
        self.assertEqual(task.updated_by, os.getlogin())

    def test_a_completed_task_has_a_completed_at_timestamp(self):
        task = self._db.find(Task, 1)
        self._db.complete(Task, task.id)
        task = self._db.find(Task, 1)
        self.assertIsNotNone(task.completed_at)

    def test_an_incomplete_task_does_not_have_a_completed_at_timestamp(self):
        task = self._db.find(Task, 1)
        self._db.incomplete(Task, task.id)
        task = self._db.find(Task, 1)
        self.assertIsNone(task.completed_at)

    def test_a_task_can_be_edited(self):
        task = self._db.find(Task, 1)

        data = {"description": "a task"}
        self._db.edit(Task, task.id, data)
        edited = self._db.find(Task, task.id)

        self.assertEqual(data["description"], edited.description)
