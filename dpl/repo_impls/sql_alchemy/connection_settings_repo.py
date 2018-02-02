from dpl.repos.abs_con_settings_repo import AbsConnectionSettingsRepository, ConnectionSettings

from .session_manager import SessionManager
from .base_repository import BaseRepository


class ConnectionSettingsRepository(BaseRepository[ConnectionSettings], AbsConnectionSettingsRepository):
    """
    An implementation of SQLAlchemy-based storage
    of ConnectionSettingsRepository
    """
    def __init__(self, session_manager: SessionManager):
        """
        Constructor. Receives an instance of SessionManager
        to be used and saves a link to it to the internal
        variable.

        :param session_manager: an instance of SessionManager
               to be used for requesting SQLAlchemy Sessions
        """
        super().__init__(session_manager, stored_cls=ConnectionSettings)

    def select_by_integration(self, integration_id: str):  # -> Collection[ConnectionSettings]:
        """
        Selects and returns settings of all Connections that
        belong to (are implemented in) the specified Integration

        :param integration_id: an identifier of Integration
               in interest
        :return: a collection of ConnectionSettings related to
                 the specified Integration
        """
        return self._session.query(self._stored_cls).filter_by(_integration=integration_id).all()
