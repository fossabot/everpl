import weakref
from typing import TypeVar, Optional, MutableSet, Type
from functools import partial

import sqlalchemy.event

from dpl.model.domain_id import TDomainId
from dpl.model.base_entity import BaseEntity
from dpl.repos.observable_repository import (
    ObservableRepository, RepositoryEventType
)
from dpl.utils.observer import Observer
from .db_session_manager import DbSessionManager
from .base_repository import BaseRepository


TEntity = TypeVar("TEntity", bound=BaseEntity)


class BaseObservableRepository(BaseRepository[TEntity], ObservableRepository):
    """
    A base implementation of SQLAlchemy repository which also implements
    an ObservableRepository interface
    """
    def __init__(
            self, session_manager: DbSessionManager,
            stored_cls: Type[TEntity]
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
        super().__init__(session_manager, stored_cls)

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
            event_type=RepositoryEventType.added
        )

        modified_listener = partial(
            self._db_event_handler,
            event_type=RepositoryEventType.modified
        )

        deleted_listener = partial(
            self._db_event_handler,
            event_type=RepositoryEventType.deleted
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
            self, mapper, connection,
            target: TEntity, event_type: RepositoryEventType
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
            self, object_id: TDomainId, event_type: RepositoryEventType,
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
                object_id=object_id,
                object_ref=object_ref
            )
