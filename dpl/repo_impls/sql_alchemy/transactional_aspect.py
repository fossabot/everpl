"""
This module contains a definition of transactional aspect -
a factory of interceptor methods which will open a DB
transaction before a method will be started, commit it on
a successful execution, rollbacks if any exception was raised
and closes after method execution regardless of results of
the execution
"""

from typing import Callable

from .db_session_manager import DbSessionManager


class TransactionalAspect(object):
    """
    A callable factory class that contains a definition of
    a transactional advice. Such advice contains a logic
    of managing of DB transactions, i.e. opens, commits,
    rollbacks or closes a transaction regarding of the result
    of execution of intercepted (wrapped) method
    """
    def __init__(self, session_manager: DbSessionManager):
        """
        Constructor. Accepts an instance of DbSessionManager
        that manages DB transactions

        :param session_manager: an instance of DbSessionManager,
               an object which contains a current transaction
               and allows to manage them
        """
        self._session_manager = session_manager

    def __call__(self, wrapped_f: Callable) -> Callable:
        """
        Returns a new callable which wraps the specified
        wrapped_f callable with transactional logic

        :param wrapped_f: a callable to be wrapped
        :return: a new callable which wraps the specified one
        """

        def _transactional_advice(*args, **kwargs):
            """
            A transactional advice. Defines a logic of transaction
            management. Creates a new transaction before method
            execution, closes it after after method execution,
            performs commit and rollback if needed, returns a value
            returned by the wrapped callable

            :param args: positional arguments to be passed to the
                   wrapped callable
            :param kwargs: keyword arguments to be passed to the
                   wrapped callable
            :return: the same value as was returned by the wrapped
                     callable
            :raises: the same exceptions as was raised by the wrapped
                     callable
            """
            session = self._session_manager.get_session()

            try:  # try to execute the wrapped callable
                result = wrapped_f(*args, **kwargs)

            except Exception as e:  # if any exception was raised...
                session.rollback()  # ...rollback any changes...
                raise e  # and re-raise an original exception

            else:  # if no exceptions was raised...
                session.commit()  # ... commit changes

            finally:  # after execution of the wrapped callable...
                session.close()  # ...close session...
                self._session_manager.remove_session()  # ...and remove it from SessionManager

            # only if no exceptions was raised...
            return result  # ...return a value returned by the wrapped callable

        return _transactional_advice
