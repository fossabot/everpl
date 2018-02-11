from sqlalchemy.engine import Connectable
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from dpl.utils.get_concurrent_identity import get_concurrent_identity

import logging

LOGGER = logging.getLogger(__name__)


class DbSessionManager(object):
    """
    DbSession manager is a class which is responsible for
    providing of database Session instances, individual for each
    thread and for each coroutine
    """
    def __init__(self, engine: Connectable):
        """
        Constructor. Receives an engine which will be
        bound with all Sessions that will be created.
        Initializes Session factory and a scoped session

        :param engine: an instance of Connectable class
               that will be used for DB connection and
               will be bound with any new Session created
               by this SessionManager object
        """
        self._session_factory = sessionmaker(bind=engine)
        self._scoped_session = scoped_session(
            session_factory=self._session_factory,
            scopefunc=get_concurrent_identity
        )

    def get_session(self) -> Session:
        """
        Returns an instance of Session to the caller.
        And at the same time each Thread or Task will get
        a different one

        :return: an instance of Session
        """
        logging.debug("Requested a new session by: %s" % get_concurrent_identity())

        return self._scoped_session()

    def remove_session(self) -> None:
        """
        Removes the current used session from the registry

        :return: None
        """
        logging.debug("Asked to remove session for: %s" % get_concurrent_identity())

        self._scoped_session.remove()
