"""
This module contains unit tests for an in-memory ThingRepository implementation
"""

import unittest
import uuid
import weakref
from unittest.mock import Mock

from dpl.connections import Connection
from dpl.things.thing import Thing
from dpl.repo_impls.in_memory.thing_repository import ThingRepository
from dpl.utils.observer import Observer
from dpl.repos.observable_repository import RepositoryEventType


class TestThingRepository(unittest.TestCase):
    def setUp(self):
        self.con_mock = Mock(spec_set=Connection)  # type: Connection
        self.thing_id = uuid.uuid4()
        self.thing_ins = Thing(
            domain_id=self.thing_id,
            con_instance=self.con_mock,
            con_params={}
        )

        self.filled_thing_repo = ThingRepository()
        self.filled_thing_repo.add(self.thing_ins)
        self.observer = Mock(spec_set=Observer)  # type: Observer
        self.observer_callback = self.observer.update  # type: Mock
        self.filled_thing_repo.subscribe(self.observer)

    def test_init(self):
        thing_repo = ThingRepository()

        self.assertEqual(
            0, thing_repo.count()
        )

        self.assertFalse(  # assert that an empty container was returned
            thing_repo.load_all()
        )

    def test_add_element(self):
        thing_repo = ThingRepository()

        thing_repo.subscribe(self.observer)
        self.observer_callback.assert_not_called()

        thing_repo.add(self.thing_ins)

        self.assertEqual(
            1, thing_repo.count()
        )
        self.assertIs(
            thing_repo.load(self.thing_id), self.thing_ins
        )

        all_things = thing_repo.load_all()

        self.assertEqual(
            thing_repo.count(),
            len(all_things)
        )
        self.assertIn(
            self.thing_ins, all_things
        )

        self.observer_callback.assert_called_once_with(
            source=weakref.proxy(thing_repo),
            event_type=RepositoryEventType.added,
            object_id=self.thing_id,
            object_ref=weakref.proxy(self.thing_ins)
        )

    def test_delete_element(self):
        assert self.filled_thing_repo.count() == 1
        assert self.thing_ins in self.filled_thing_repo.load_all()

        self.filled_thing_repo.delete(domain_id=self.thing_id)

        self.assertEqual(
            0, self.filled_thing_repo.count()
        )
        self.assertFalse(
            self.filled_thing_repo.load_all()
        )
        self.assertIsNone(
            self.filled_thing_repo.load(self.thing_id)
        )

        self.observer_callback.assert_called_once_with(
            source=weakref.proxy(self.filled_thing_repo),
            event_type=RepositoryEventType.deleted,
            object_id=self.thing_id,
            object_ref=None
        )

    def test_modify_element(self):
        assert self.thing_ins in self.filled_thing_repo.load_all()

        self.thing_ins._apply_update()

        self.observer_callback.assert_called_once_with(
            source=weakref.proxy(self.filled_thing_repo),
            event_type=RepositoryEventType.modified,
            object_id=self.thing_id,
            object_ref=self.thing_ins
        )
