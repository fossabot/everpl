"""
This module contains a definition of Event - a structure-like class that
carries information about events that happened in the system
"""
import time


class Event(object):
    """
    Event class carries information about an event happened in the system.

    Base (this) Event class contains only two fields:

    - timestamp - when event occurred;
    - topic - what the topic (category) of this Event.

    All the remaining fields are defined by Event subclasses.
    """
    def __init__(self, topic: str):
        """
        Constructor. Receives a topic - a hierarchical identifier of a theme,
        topic, event type this Event belongs to.

        :param topic: a hierarchical topic (category) this Event belongs to
        """
        self._timestamp = time.time()
        self._topic = topic

    @property
    def timestamp(self) -> float:
        """
        Returns a time moment when this Event was generated

        :return: a time moment when this Event was generated in
                 UNIX time format (floating point number)
        """
        return self._timestamp

    @property
    def topic(self) -> str:
        """
        Returns a topic of this Event

        :return: a hierarchical topic (category) this Event belongs to
        """
        return self._topic
