import weakref
from typing import Optional, Sequence, MutableSequence, MutableSet

from dpl.utils.observer import Observer
from dpl.model.domain_id import TDomainId
from dpl.things.thing import Thing
from .base_repository import BaseRepository
from dpl.repos.observable_repository import EventType
from dpl.repos.abs_thing_repository import AbsThingRepository


class ThingRepository(BaseRepository[Thing], AbsThingRepository):
    """
    An implementation of Things storage
    """
    def __init__(self):
        super().__init__()
        self._observers = set()  # type: MutableSet[Observer]
        self._weak_self = weakref.proxy(self)

    def add(self, new_obj: Thing) -> None:
        """
        Add a new element to the storage

        In addition to the base repository behaviour subscribes itself on any
        updates to a Thing and notifies all Observers that a new object was
        added to the Repository

        :param new_obj: new object to be stored
        :return: None
        """
        super().add(new_obj)
        new_obj.on_update = self._thing_modified_callback
        self._notify_added(thing=new_obj)

    def delete(self, domain_id: TDomainId) -> None:
        """
        Removes an element with the specified ID from the storage

        In addition to the base repository behaviour removes a subscription on
        updates to a Thing and notifies all Observers that an object was
        deleted from the Repository

        :param domain_id: an ID of element to be removed
        :return: None
        """
        thing = self.load(domain_id)
        thing.on_update = None
        super().delete(domain_id)
        self._notify_deleted(thing_id=domain_id)

    def _notify_added(self, thing: Thing) -> None:
        """
        Notifies all Observers that the specified Thing was added to this Repo

        :param thing: an instance of a Thing that was added
        :return: None
        """
        self._notify(
            object_id=thing.domain_id,
            event_type=EventType.added,
            object_ref=weakref.proxy(thing)
        )

    def _notify_deleted(self, thing_id: TDomainId) -> None:
        """
        Notifies all Observers that a Thing with the specified ID was deleted
        from a repository

        :param thing_id: an identifier of a Thing that was deleted
        :return: None
        """
        self._notify(
            object_id=thing_id,
            event_type=EventType.deleted,
            object_ref=None
        )

    def _thing_modified_callback(self, thing: Thing) -> None:
        """
        A callback to be called by instances of a Thing when any of them will
        be modified

        :param thing: an instance of Thing that was modified
        :return: None
        """
        self._notify(
            object_id=thing.domain_id,
            event_type=EventType.modified,
            object_ref=weakref.proxy(thing)
        )

    def subscribe(self, observer: Observer) -> None:
        """
        Adds the specified Observer to the list of subscribers

        :param observer: an instance of Observer to be added
        :return: None
        """
        self._observers.add(observer)

    def unsubscribe(self, observer: Observer) -> None:
        """
        Removes the specified  Observer from the list of subscribers

        :param observer: an instance of Observer to be deleted
        :return: None
        """
        self._observers.discard(observer)

    def _notify(
            self, object_id: TDomainId, event_type: EventType,
            object_ref: Optional[Thing]
    ):
        """
        Notifies all of the subscribers that an object was modified in,
        added to or deleted from this Repository

        :param object_id: an identifier of an altered object
        :param event_type: enum value, specifies what happened to the object
        :param object_ref: a reference to the altered object or None if it was
               deleted
        :return: None
        """
        for o in self._observers:
            o.update(
                source=self._weak_self,
                event_type=event_type,
                object_id=object_id,
                object_ref=object_ref
            )

    def select_by_placement(self, placement_id: Optional[TDomainId]) -> Sequence[Thing]:
        """
        Fetches a collection of identifiers of all Things
        that are present in the specified placement

        :param placement_id: an identifier of Placement to be
               used for filtering; None (null) can be used as
               a value of parameter to fetch a list of Things
               that don't belong to any Placement
        :return: a collection of all things that belong to
                 the specified placement
        """
        # FIXME: Replace by native database filtering when DB
        # of settings will be added
        result = list()  # type: MutableSequence[Thing]

        for thing in self._objects.values():
            if thing.metadata.get('placement') == placement_id:
                result.append(thing)

        return result

    def select_by_connection(self, connection_id: TDomainId) -> Sequence[Thing]:
        """
        Fetches a collection of identifiers of all Things that
        use the specified Connection

        :param connection_id: an ID of Connection of interest
        :return: a collection of all Things that use the
                 specified connection
        """
        # FIXME: Replace by native database filtering when DB
        # of settings will be added
        result = list()  # type: MutableSequence[Thing]

        for thing in self._objects.values():
            if thing.metadata.get('con_id') == connection_id:
                result.append(thing)

        return result
