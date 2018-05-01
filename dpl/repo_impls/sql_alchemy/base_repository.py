import weakref
from typing import (
    TypeVar, Optional, MutableMapping, Sequence, Iterable, Type,
    MutableSet
)
from functools import partial

from sqlalchemy import func
from sqlalchemy.orm import Session
import sqlalchemy.event

from dpl.utils.flatten import flatten
from dpl.model.domain_id import TDomainId
from dpl.model.base_entity import BaseEntity
from dpl.repos.abs_repository import AbsRepository
from dpl.repos.observable_repository import ObservableRepository, EventType
from dpl.utils.observer import Observer
from .db_session_manager import DbSessionManager


TEntity = TypeVar("TEntity", bound=BaseEntity)
TEntityCollection = MutableMapping[TDomainId, TEntity]


class BaseRepository(AbsRepository[TEntity], ObservableRepository[TEntity]):
    """
    A base implementation of SQLAlchemy-based repository
    """
    def __init__(
            self, session_manager: DbSessionManager, stored_cls: Type[TEntity]
    ):
        """
        Constructor. Receives an instance of SessionManager
        to be used and saves a link to it to the internal
        variable. Also it receives a type of stored objects
        used for fetching from data from appropriate DB table

        :param session_manager: an instance of SessionManager
               to be used for requesting SQLAlchemy Sessions
        :param stored_cls: a type of objects that to stored
               in this Repository; this object must to be
               associated with a DB table by means of
               SQLAlchemy ORM mappers
        """
        self._session_manager = session_manager
        self._stored_cls = stored_cls
        self._observers = set()  # type: MutableSet[Observer]
        self._weak_self = weakref.proxy(self)

        self._setup_object_event_handlers()

    def _setup_object_event_handlers(self) -> None:
        """
        Performs setup of handlers for object addition, modification and
        removal for SQLAlchemy-mapped class

        :return: None
        """
        added_listener = partial(
            self._db_event_handler,
            event_type=EventType.added
        )

        modified_listener = partial(
            self._db_event_handler,
            event_type=EventType.modified
        )

        deleted_listener = partial(
            self._db_event_handler,
            event_type=EventType.deleted
        )

        sqlalchemy.event.listen(
            target=self._stored_cls,
            identifier='after_insert',
            fn=added_listener
        )

        sqlalchemy.event.listen(
            target=self._stored_cls,
            identifier='after_update',
            fn=modified_listener
        )

        sqlalchemy.event.listen(
            target=self._stored_cls,
            identifier='after_delete',
            fn=deleted_listener
        )

    def _db_event_handler(
            self, mapper, connection, target: TEntity, event_type: EventType
    ) -> None:
        """
        A handler method to be called of any of the objects controlled by
        this Repository will be added to, modified in or deleted from the DB

        :param mapper: an instance of SQLAlchemy DB Mapper
        :param connection: an instance of SQLAlchemy DB Connection
        :param target: an object that was altered
        :param event_type: Enum value; determines if the object was added,
               modified or removed
        :return: None
        """
        self._notify(
            object_id=target.domain_id,
            event_type=event_type,
            object_ref=weakref.proxy(target)
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
            object_ref: Optional[TEntity]
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
                object_ref=object_ref
            )

    @property
    def _session(self) -> Session:
        """
        Receives an instance of Session from SessionManager

        :return: an instance of Session
        """
        return self._session_manager.get_session()

    def count(self):
        """
        Counts a number of elements stored in this repository

        :return: integer, a number of elements stored in this
                 repository
        """
        return self._session.query(
            func.count('*')
        ).select_from(self._stored_cls).scalar()

    def load(self, domain_id: TDomainId) -> Optional[TEntity]:
        """
        Loads a Thing from internal storage and returns it
        by its identifier

        :param domain_id: an ID of Thing to fetched
        :return: a Thing with a corresponding identifier
                 or None (null) if it wasn't found
        """
        return self._session.query(self._stored_cls).get(domain_id)

    def load_all(self) -> Sequence[TEntity]:
        """
        Returns all Things that are stored in this Repository

        :return: a collection of stored objects
        """
        return self._session.query(self._stored_cls).all()

    def select_all_domain_ids(self) -> Iterable[TDomainId]:
        """
        Returns identifiers of all Things that are stored
        in this Repository

        :return: a collection of stored objects
        """
        query = self._session.query(
            self._stored_cls._domain_id
        )

        return flatten(query.all())

    def add(self, new_obj: TEntity) -> None:
        """
        Add a new element to the storage

        :param new_obj: new object to be stored
        :return: None
        """
        self._session.add(new_obj)

    # FIXME: CC28: Pass an object itself instead of its identifier
    def delete(self, domain_id: TDomainId) -> None:
        """
        Removes an element with the specified ID from the
        storage

        :param domain_id: an ID of element to be removed
        :return: None
        """
        query = self._session.query(self._stored_cls)
        on_delete = query.filter(self._stored_cls._domain_id == domain_id)
        on_delete.delete()
