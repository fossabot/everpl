from dpl.model.domain_id import TDomainId
from dpl.repos.abs_routine_repo import AbsRoutineRepo, Routine

from .db_session_manager import DbSessionManager
from .base_repository import BaseRepository


class ThingSettingsRepository(BaseRepository[Routine], AbsRoutineRepo):
    """
    An implementation of SQLAlchemy-based storage of Routines
    """
    def __init__(self, session_manager: DbSessionManager):
        """
        Constructor. Receives an instance of SessionManager to be used and
        saves a link to it to the internal variable.

        :param session_manager: an instance of SessionManager to be used
               for requesting SQLAlchemy Sessions
        """
        super().__init__(session_manager, stored_cls=Routine)

    def select_by_author(self, author_id: TDomainId):
        return self._session.query(self._stored_cls)\
            .filter_by(_author=author_id)\
            .all()
