import uuid

from dpl.model.domain_id import TDomainId
from dpl.auth.session import Session
from dpl.dtos.dto_builder import build_dto
from dpl.dtos.session_dto import SessionDto
from dpl.repos.abs_session_repository import AbsSessionRepository
from dpl.services.abs_session_service import AbsSessionService

from .base_service import BaseService


class SessionService(AbsSessionService, BaseService[SessionDto]):
    """
    This is an implementation of a SessionService -
    a class that manages all Sessions in the system
    """
    def __init__(self, session_repo: AbsSessionRepository):
        """
        Constructor. Receives an instance of SessionRepository
        which will be used to store all Sessions and fetch them

        :param session_repo: an instance of a SessionRepository
        """
        self._sessions = session_repo

    def view_all(self):  # -> Collection[SessionDto]:
        """
        Fetch a full list of DTOs of all stored objects

        :return: a collection of DTOs
        """
        return [build_dto(i) for i in self._sessions.load_all()]

    def view(self, domain_id: TDomainId) -> SessionDto:
        """
        Fetch a DTO of stored object by the ID specified

        :param domain_id: id of object to be fetched
        :return: a DTO of stored object
        :raises ServiceResolutionError: if the entity with
                the specified ID can't be found
        """
        return build_dto(
            self._sessions.load(domain_id)
        )

    def remove(self, domain_id: TDomainId) -> None:
        """
        REMOVES an Entity with the specified ID altogether
        from the system

        :param domain_id: an identifier of Entity to be deleted
        :return: None
        :raises ServiceResolutionError: if the entity with
                the specified ID can't be found
        :raises ServiceEntityLinkError: if the specified can't
                be removed because some other entity is linked
                (uses or refers) to it
        """
        self._sessions.delete(domain_id)

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
        session = Session(
            domain_id=uuid.uuid4().hex,
            user_id=user_id,
            client_info=client_info,
            client_ip=client_ip
        )

        self._sessions.add(session)

        return session.domain_id

    def get_access_key(self, by_session: TDomainId) -> str:
        """
        Allows to extract an access key from the specified Session

        WARNING: Must NOT to be directly exposed to the API

        :param by_session: an identifier of Session which contains
               a needed access key
        :return: an access key associated with the specified Session
        """
        session = self._resolve_entity(
            repository=self._sessions,
            domain_id=by_session
        )

        return session.access_token

    def view_by_user(self, user_id: TDomainId):  # -> Collection[SessionDto]
        """
        Returns a collection of Sessions (Session DTOs to
        be exact) that are associated with the specified
        User

        :param user_id: an identifier of the User in question
        :return: a collection of SessionDto objects
        """
        resolved = self._sessions.select_by_user(user_id)

        return [build_dto(i) for i in resolved]

    def view_by_access_key(self, access_key: str) -> SessionDto:
        """
        Allows to determine and fetch a Session which contains
        the specified access_key

        :param access_key: an access key associated with Session
        :return: Session DTO
        """
        resolved = self._sessions.find_by_access_token(access_key)

        return build_dto(resolved)

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
        resolved = self._sessions.select_older_than(timestamp)

        return [build_dto(i) for i in resolved]

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
        resolved = self._sessions.select_by_user(for_user)  # type\: Collection[Session]

        if excluding is None:
            on_removal = [i.domain_id for i in resolved]  # small speedup on comparison
        else:
            on_removal = [i.domain_id for i in resolved if i.access_token != excluding]

        for i in on_removal:
            self._sessions.delete(i)
