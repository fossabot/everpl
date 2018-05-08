"""
This module contains a base Observable implementation with registration of
subscribers and mostly nothing else
"""

import weakref

from .observer import Observer
from .observable import Observable


class BaseObservableMixin(Observable):
    """
    A base implementation of Observer interface. Handles registration of
    subscribers (Observers) and their removal
    """
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
