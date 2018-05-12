"""
This module contains a definition of ObjectRelatedEvent - a class for events
that are related to some objects (i.e. to their creation, deletion or
modification).
"""
from typing import Optional

from dpl.dtos.base_dto import BaseDto
from .event import Event


class ObjectRelatedEvent(Event):
    """
    Contains information about an event that happened with some object
    """
    def __init__(self, topic: str, object_dto: Optional[BaseDto]):
        """
        Constructor. Receives information about a topic of event (constructed
        like ``object_category/object_id/what_changed`` and an object DTO -
        representation of the current state of the object.

        :param topic: a topic (category) of this Event
        :param object_dto: a current state of an object or None if it was
               deleted
        """
        super().__init__(topic)
        self._object_dto = object_dto

    @property
    def object_dto(self) -> Optional[BaseDto]:
        """
        Returns the current DTO (representation) of the object this Event is
        related to

        :return: the current DTO (representation) of the object this Event is
                 related to
        """
        return self._object_dto
