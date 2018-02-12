from dpl.model.domain_id import TDomainId
from .abs_entity_service import AbsEntityService
from dpl.dtos.session_dto import SessionDto


class AbsSessionService(AbsEntityService[SessionDto]):
    """
    A base class for all SessionService implementations
    """
    def create_session(self, user_id: TDomainId, client_info: str, client_ip: str) -> TDomainId:
        """
        Creates a new object of Session for the specified User

        :param user_id: an identifier of User for which the Session
               was requested to be created
        :param client_info: user-agent or other information which
               allows to identify a client device or application
               which requested session creation
        :param client_ip: an IP of the client device which requested
               Session creation
        :return: an identifier of the created Session
        """
        raise NotImplementedError()

    def get_access_token(self, by_session: TDomainId) -> str:
        """
        Allows to extract an access token from the specified Session

        WARNING: Must NOT to be directly exposed to the API

        :param by_session: an identifier of Session which contains
               a needed access token
        :return: an access token associated with the specified Session
        """
        raise NotImplementedError()

    def view_by_user(self, user_id: TDomainId):  # -> Collection[SessionDto]
        """
        Returns a collection of Sessions (Session DTOs to
        be exact) that are associated with the specified
        User

        :param user_id: an identifier of the User in question
        :return: a collection of SessionDto objects
        """
        raise NotImplementedError()

    def view_by_access_token(self, access_token: str) -> SessionDto:
        """
        Allows to determine and fetch a Session which contains
        the specified access token

        :param access_token: an access token associated with Session
        :return: Session DTO
        """
        raise NotImplementedError()

    def view_older_than(self, timestamp: float):  # -> Collection[SessionDto]
        """
        Allows to fetch all Sessions that was created before
        the specified point in time (UNIX time)

        :param timestamp: UNIX time, maximum value of the
               time_created field
        :return: a collection of Sessions (their DTOs, to be
                 exact) that was created before the specified
                 point in time
        """
        raise NotImplementedError()

    def close_all_user_sessions(self, for_user: TDomainId, excluding: TDomainId = None) -> None:
        """
        Closes (i.e. deletes) all sessions for the specified User.
        Have an optional "excluding" argument which allows to
        specify exactly one (i.e. current) Session to be closed.

        :param for_user: an identifier of User for which all the
               Sessions must to be closed (deleted)
        :param excluding: optional argument, an identifier of
               Session which must NOT to be closed
        :return: None
        """
        raise NotImplementedError()
