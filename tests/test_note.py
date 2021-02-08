from unittest import TestCase
from models.note import Note
from models.item import Item
from data.datapersistence import SqlitePersistence
import os


class TestNote(TestCase):
    _item = Item()
    _note = Note()
    _db = SqlitePersistence(":memory:")

    def setUp(self):
        self._item.rig = "X01"
        self._item.description = "Something to handover"
        self._item.case = "CAS-12345"
        self._db.save(self._item)

        self._note.description = "Some update"
        self._note.item_id = 1
        self._db.save(self._note)

    def test_a_note_has_a_description(self):
        note = self._db.find(Note, 1)
        self.assertEqual(note.description, "Some update")

    def test_a_note_has_an_item(self):
        note = self._db.find(Note, 1)
        self.assertEqual(note.item.description, self._item.description)

    def test_a_saved_note_has_a_created_by_timestamp(self):
        note = self._db.find(Note, 1)
        self.assertIsNotNone(note.created_by)

    def test_a_saved_note_has_an_updated_by_timestamp(self):
        note = self._db.find(Note, 1)
        self.assertIsNotNone(note.updated_by)

    def test_a_saved_note_has_a_created_by(self):
        note = self._db.find(Note, 1)
        self.assertEqual(note.created_by, os.getlogin())

    def test_a_saved_note_has_an_updated_by(self):
        note = self._db.find(Note, 1)
        self.assertEqual(note.updated_by, os.getlogin())
