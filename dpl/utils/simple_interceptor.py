import inspect
import functools
from typing import TypeVar, Generic, Callable


T = TypeVar('T')


def aspect_example(original_f: Callable) -> Callable:
    """
    An example of a so-called Aspect / advice provider /
    decorator function

    :param original_f: a function to be wrapped
    :return: a function to be called instead of the wrapped one
    """
    @functools.wraps(original_f)
    def _advice(*args, **kwargs):
        """
        Implementation detail. A definition of a function
        to be called instead of the wrapped one

        :param args: positional arguments received on call
        :param kwargs: keyword arguments received on call
        :return: a value that was returned by an original
                 function or some other acceptable value
        """
        # some logic to be executed before an actual call
        print("Hi from an Advice!")

        try:
            result = original_f(*args, **kwargs)

        # Some exception handling logic (code to be executed
        # on a fail)
        except Exception as e:
            raise e

        # Some logic to be executed after a call regardless
        # of the execution result
        finally:
            pass

        # some logic to be executed in a case of a successful call
        print("Bye from an Advice!")

        # return execution result here
        return result

    return _advice


class SimpleInterceptor(Generic[T]):
    """
    SimpleInterceptor is a class which implements an
    Interceptor pattern.

    SimpleInterceptor class is a class that mimics an interface
    of another class, intercepts calls to the methods of
    original class and are able to execute some code before,
    after or instead the original method.

    .. WARNING: SimpleInterceptor only mimics a set of
       public methods of the specified object (in the
       current implementation). Properties, private methods
       and other fields will **not** be available for access
       in SimpleInterceptor instances
    """
    def __init__(self, wrapped: T, aspect: Callable):
        """
        Constructor if an interceptor object.

        :param wrapped: an instance to be wrapped by
               SimpleInterceptor
        :param aspect: a decorator function or other callable to
               be used for wrapping; this decorator function
               must to accept a callable to be wrapped as the
               first argument and return a function to be called
               instead of the original callable (instead of a
               callable to be wrapped)
        """
        self._wrapped = wrapped
        self._aspect = aspect

        self.__init_interceptor_members()

    def __init_interceptor_members(self) -> None:
        """
        Implementation detail. Initializes members of Interceptor
        to mimic a public interface of the original object

        :return: None
        """
        # FIXME: CC31: Consider to add a support of class methods,
        # properties and other methods

        members = inspect.getmembers(self._wrapped, predicate=inspect.ismethod)

        for name, member in members:
            if name.startswith("_"):
                continue
            else:  # intercept only public methods
                setattr(self, name, self._aspect(member))

    def __getattr__(self, item: str):
        """
        This method is invoked only in a case when the requested
        method wasn't found by usual means (i.e. in existing
        attribute of this interceptor).

        Looks for an attribute in the original (wrapped) object.
        If an attribute was found and is a callable, then it is
        wrapped with an aspect, saved to the interceptor attribute
        for future uses and returned to the caller. In all other
        cases an AttributeError will be raised.

        Is handy for the usage of interceptors with Mocks.

        :param item: a name of an attribute to be fetched
        :return: an attribute value
        """
        wrapped_attr = getattr(self._wrapped, item)

        if callable(wrapped_attr):
            setattr(self, item, self._aspect(wrapped_attr))

        return super().__getattribute__(item)


