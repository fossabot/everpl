from typing import Optional, Callable


class UpdateCallback(object):
    """
    Implementations of UpdateCallback interface has an on_update property
    that allows to define a single callback to be called on each update
    of a Thing.

    A callback to be registered must to accept a single parameter: a weak
    reference to the event source (i.e. to the updated Thing)
    """
    @property
    def on_update(self) -> Optional[Callable]:
        """
        Returns a callable that is currently registered to be called on each
        update of this object

        :return: a callable that is currently registered to be called on each
                 update of this object; or None if a callable wasn't set yet
        """
        raise NotImplementedError()

    @on_update.setter
    def on_update(self, callback: Optional[Callable]) -> None:
        """
        Allows to set a callable to be called on each update of this object.
        This callable must to accept a reference to the event source (i.e. to
        this object)

        :param callback: a new callback to be set or None to unset a callback
        :return: None
        """
        raise NotImplementedError()
