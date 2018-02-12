from typing import Optional

from .abs_repository import AbsRepository
from dpl.model.domain_id import TDomainId
from dpl.auth.session import Session


class AbsSessionRepository(AbsRepository[Session]):
    """
    Pure abstract base implementation of Repository
    containing Sessions.

    Contains declarations of methods that must to be present
    in specific implementations of this repository
    """
    def select_by_user(self, user_id: TDomainId):  # -> Collection[Session]
        """
        Returns all sessions created for the specified User

        :param user_id: an identifier of User in question
        :return: a collection of Sessions created for the
                 specified User
        """
        raise NotImplementedError()

    def select_older_than(self, timestamp: float):  # -> Collection[Session]
        """
        Returns all sessions that was created before the
        specified time in UNIX time format

        :param timestamp: maximum value of Session creation time
        :return: a collections of Sessions that was created
                 before the specified time moment
        """
        raise NotImplementedError()

    def find_by_access_token(self, access_token: str) -> Optional[Session]:
        """
        Returns a Session object by an associated access token

        :param access_token: an access token which was associated
               with the Session to be returned
        :return: a Session with the specified access token or
                 None if such Session was not found
        """
        raise NotImplementedError()
