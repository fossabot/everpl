from typing import Optional, MutableMapping, MutableSet

from dpl.model.domain_id import TDomainId
from dpl.auth.session import Session
from dpl.repos.abs_session_repository import AbsSessionRepository
from .base_repository import BaseRepository


class SessionRepository(BaseRepository[Session], AbsSessionRepository):
    """
    An implementation of in-memory storage of Sessions
    """
    def __init__(self):
        """
        Constructor. Initializes internal in-memory storage
        """
        super().__init__()
        self._sessions_by_user = dict()  # type: MutableMapping[str, MutableSet[Session]]
        self._sessions_by_access_token = dict()  # type: MutableMapping[str, Session]

    def add(self, new_obj: Session) -> None:
        """
        Add a new element to the storage

        :param new_obj: new object to be stored
        :return: None
        """
        super().add(new_obj)

        sessions_of_user = self._sessions_by_user.get(new_obj.user_id)

        if sessions_of_user is None:
            sessions_of_user = set()
            self._sessions_by_user[new_obj.user_id] = sessions_of_user

        sessions_of_user.add(new_obj)

        self._sessions_by_access_token[new_obj.access_token] = new_obj

    def delete(self, domain_id: TDomainId) -> None:
        """
        Removes an element with the specified ID from the
        storage

        :param domain_id: an ID of element to be removed
        :return: None
        """
        obj = self.load(domain_id)

        self._sessions_by_access_token.pop(obj.access_token)
        sessions_of_user = self._sessions_by_user[obj.user_id]
        sessions_of_user.remove(obj)

        super().delete(domain_id)

    def select_by_user(self, user_id: TDomainId):  # -> Collection[Session]
        """
        Returns all sessions created for the specified User

        :param user_id: an identifier of User in question
        :return: a collection of Sessions created for the
                 specified User
        """
        return self._sessions_by_user.get(user_id, default=tuple())

    def select_older_than(self, timestamp: float):  # -> Collection[Session]
        """
        Returns all sessions that was created before the
        specified time in UNIX time format

        :param timestamp: maximum value of Session creation time
        :return: a collections of Sessions that was created
                 before the specified time moment
        """
        return [i for i in self._objects.values() if i.time_created <= timestamp]

    def find_by_access_token(self, access_token: str) -> Optional[Session]:
        """
        Returns a Session object by an associated access token

        :param access_token: an access token which was associated
               with the Session to be returned
        :return: a Session with the specified access token or
                 None if such Session was not found
        """
        return self._sessions_by_access_token.get(access_token)
