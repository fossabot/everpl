"""
This module contains a definition of EventHub - a central place for processing
of all events in the system
"""
import functools
from typing import Type, MutableSet, Callable

from dpl.utils.observer import Observer
from dpl.utils.observable import Observable
from dpl.events.event import Event


def _convert_to_event(source: Observable, *args, **kwargs) -> Event:
    """
    A skeleton of a function that converts the specified data received from the
    specified event source to an instance of Event

    :param source: a source of this event
    :param args: positional arguments, an information about event
    :param kwargs: keyword arguments, an information about event
    :return: an instance of Event
    """
    raise NotImplementedError("Failed to find a converter for the specified"
                              "source: %s" % source)


class EventHub(Observer, Observable):
    """
    EventHub is a central place for all events in the system. It's responsible
    for pre-processing of events, coming from all the services, APIs and other
    sources, and their distribution to other subscribers (like services, APIs,
    loggers and other interested parties
    """
    def __init__(self):
        """
        Constructor. Initializes internal variables
        """
        self._observers = set()  # type: MutableSet[Observer]
        self._converter = functools.singledispatch(_convert_to_event)

    def update(self, source: Observable, *args, **kwargs) -> None:
        """
        A method to be called by event sources if any event was generated.
        The source of event is determined by the first parameter of
        this method. The number and an exact set of parameters is determined
        by the event source. The way of handling such parameters is determined
        registered event handlers.

        :param source: an object which generated an event
        :param args: positional arguments, information about event
        :param kwargs: keyword arguments, information about event
        :return: None
        """
        event = self._converter(source, *args, **kwargs)
        self._notify(event)

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

    def _notify(self, event: Event) -> None:
        """
        Sends the specified event to all subscribers of EventHub

        :param event: an event to be broadcasted
        :return: None
        """
        for observer in self._observers:
            observer.update(self, event)

    def register_handler(self, source_type: Type, handler: Callable) -> None:
        """
        Registers a handler method (converter) that will generate Event objects
        based on data sent by the specified type of source objects
        (Observables)

        :param source_type: a type of Observable events from which will be
               processed by the specified handler
        :param handler: a callable to process events from the specified sources
        :return: None
        """
        self._converter.register(source_type, handler)
