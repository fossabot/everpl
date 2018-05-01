from .observer import Observer


class Observable(object):
    """
    Observable is an abstract class which declares the interface to be
    implemented by Observable pattern implementations. It specifies methods
    for subscription and cancelling subscriptions of Observers. And a
    protected method ``notify`` to be used for notification of Observers
    """
    def subscribe(self, observer: Observer) -> None:
        """
        Adds the specified Observer to the list of subscribers

        :param observer: an instance of Observer to be added
        :return: None
        """
        raise NotImplementedError()

    def unsubscribe(self, observer: Observer) -> None:
        """
        Removes the specified  Observer from the list of subscribers

        :param observer: an instance of Observer to be deleted
        :return: None
        """
        raise NotImplementedError()
