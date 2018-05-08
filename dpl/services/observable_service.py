from typing import TypeVar, Optional, Generic
from enum import Enum

from dpl.model.domain_id import TDomainId
from dpl.utils.observable import Observable
from .abs_entity_service import AbsEntityService


T = TypeVar('T')


class ServiceEventType(Enum):
    """
    An enumeration to define a type of event (change) happened in the Service
    """
    added = 0
    modified = 1
    deleted = 2


class ObservableService(AbsEntityService[T], Observable):
    """
    ObservableService is a declaration of an interface to be implemented
    by Observable Service. Is a sample of Observable pattern; notifies all
    subscribers (Observers) that any of the objects served by this Service
    was added, modified or deleted
    """
    def _notify(
            self, object_id: TDomainId, event_type: ServiceEventType,
            object_dto: Optional[T]
    ) -> None:
        """
        Notifies all of the subscribers that an object, controlled by this
        Service, was modified, added to or deleted from the system

        :param object_id: an identifier of an altered object
        :param event_type: enum value, specifies what happened to the object
        :param object_dto: a DTO of the altered object or None if it was
               deleted
        :return: None
        """
        raise NotImplementedError()
