from enum import Enum
from typing import TypeVar, Generic, Optional

from dpl.utils.observable import Observable
from dpl.model.domain_id import TDomainId


T = TypeVar('T')


class RepositoryEventType(Enum):
    added = 0
    modified = 1
    deleted = 2


class ObservableRepository(Observable, Generic[T]):
    """
    ObservableRepository is a declaration of an interface to be implemented
    by Observable Repositories. Is a sample of Observable pattern; notifies all
    subscribers (Observers) that any of the objects stored in the repository
    was added, modified or deleted
    """
    def _notify(
            self, object_id: TDomainId, event_type: RepositoryEventType,
            object_ref: Optional[T]
    ) -> None:
        """
        Notifies all of the subscribers that an object was modified in,
        added to or deleted from this Repository

        :param object_id: an identifier of an altered object
        :param event_type: enum value, specifies what happened to the object
        :param object_ref: a reference to the altered object or None if it was
               deleted
        :return: None
        """
        raise NotImplementedError()
