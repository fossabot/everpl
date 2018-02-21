"""
This module contains a definition of AuthContext - an
implementation of Ambient Context pattern based on a Python's
context manager
"""
import contextlib
from typing import Optional

from dpl.utils.get_concurrent_identity import get_concurrent_identity


class AuthContext(object):
    """
    AuthContext is an implementation of Ambient Context
    pattern which:

    - will save current authentication token in a temporary
      storage;
    - will allow to read currently stored token;
    - will remove a token from a temporary storage on an exit
      from a context;
    - will be used by AuthAspect for authorization and
      authentication checking.

    All received access tokens are bound to the current thread (for
    multi-threaded environments) or task (for asynchronous
    environments).
    """
    def __init__(self):
        """
        Constructor. Initializes an internal storage of tokens
        """
        # key: a thread- or task-unique identifier
        # value: a token itself
        self._tokens = dict()

    def __call__(self, token: str):
        """
        Constructs and returns a Python context manager. Adds auth
        token to the temporary storage

        :param token: an auth token to be used for the current
               Thread or Task
        :return: an instance of a Python context manager
        """
        return self._context_manager(token)

    @contextlib.contextmanager
    def _context_manager(self, token: str):
        """
        An implementation of a Python context manager. Saves the
        specified token to the temporary storage, allows for a
        code in the context to execute and finally removes an
        access token from a temporary storage

        For more information about the structure of context
        managers see Python documentation at https://goo.gl/6g7VES

        :param token: an auth token to be used for the current
               Thread or Task
        :return: None
        """
        concurrent_id = get_concurrent_identity()
        self._tokens[concurrent_id] = token

        yield

        self._tokens.pop(concurrent_id)

    @property
    def current_token(self) -> Optional[str]:
        """
        Returns an access token bound to the current Thread
        or Task. Returns None if no access token was bound

        :return: an access token which is currently bound to
                 the current Thread or Task; returns None if
                 no access token was bound
        """
        concurrent_id = get_concurrent_identity()
        return self._tokens.get(concurrent_id, default=None)
