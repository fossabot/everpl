from typing import TypeVar, Generic

T = TypeVar('T')


class Observer(Generic[T]):
    """
    Observer is an abstract class which declares the interface to be
    implemented by Observer pattern implementations. It specifies a method
    for handling of events emitted by Observers - update
    """
    def update(self, source: T, *args, **kwargs) -> None:
        """
        A method to be called by Observables on any new events emitted

        :param source: mandatory, a weak reference to the event source
        :param args: optional positional arguments with additional information
               about emitted event
        :param kwargs: optional keyword arguments with additional information
               about emitted event
        :return: None
        """
        raise NotImplementedError()
