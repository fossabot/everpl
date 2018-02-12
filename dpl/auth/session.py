import time

from dpl.utils.generate_token import generate_token
from dpl.model.domain_id import TDomainId
from dpl.model.base_entity import BaseEntity


class Session(BaseEntity):
    """
    Session represents information about current login sessions,
    i.e. which user was logged in, what device was used and when
    it happened. Also each Session contains an access token - some
    temporary key that is used for authentication of users and was
    issued to exactly one client device.
    """
    def __init__(self, domain_id: TDomainId, user_id: TDomainId, client_info: str, client_ip: str):
        """
        Creates a new Session object for the specified user and
        client device (application).

        The value of time_created field is set automatically to
        the current system time.

        :param domain_id: a unique identifier of this Session
        :param user_id: an identifier of User for which the Session
               was requested to be created
        :param client_info: user-agent or other information which
               allows to identify a client device or application
               which requested session creation
        :param client_ip: an IP of the client device which requested
               Session creation
        """
        super().__init__(domain_id)

        self._time_created = time.time()
        self._access_token = generate_token()

        self._user_id = user_id
        self._client_info = client_info
        self._client_ip = client_ip

    @property
    def time_created(self) -> float:
        """
        Returns timestamp of when the Session was created

        :return: UNIX time timestamp, in seconds from UNIX epoch
        """
        return self._time_created

    @property
    def access_token(self) -> str:
        """
        Returns an access token associated with this session.

        :return: string, an access token associated with
                 this sessions
        """
        return self._access_token

    @property
    def user_id(self) -> TDomainId:
        """
        Returns an identifier of User associated with this Session

        :return: an identifier of User associated with this Session
        """
        return self._user_id

    @property
    def client_info(self) -> str:
        """
        Returns an information about a device or application which
        requested creation of this Session (like a content of a
        User-Agent header)

        :return: an information about a device or application which
                 requested creation of the new session
        """
        return self._client_info

    @property
    def client_ip(self) -> str:
        """
        Returns an IP address of a device which requested creation of
        this Session

        :return: returns an IP address of a device which requested
        creation of this Session
        """
        return self._client_ip
