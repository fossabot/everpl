from typing import TypeVar, Optional, MutableMapping, Sequence, Iterable, Type

from sqlalchemy import func
from sqlalchemy.orm import Session

from dpl.utils.flatten import flatten
from dpl.model.domain_id import TDomainId
from dpl.model.base_entity import BaseEntity
from dpl.repos.abs_repository import AbsRepository
from .db_session_manager import DbSessionManager


TEntity = TypeVar("TEntity", bound=BaseEntity)
TEntityCollection = MutableMapping[TDomainId, TEntity]


class BaseRepository(AbsRepository[TEntity]):
    """
    A base implementation of SQLAlchemy-based repository
    """
    def __init__(self, session_manager: DbSessionManager, stored_cls: Type[TEntity]):
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
