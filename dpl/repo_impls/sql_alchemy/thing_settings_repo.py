from dpl.repos.abs_thing_settings_repo import AbsThingSettingsRepository, ThingSettings

from .session_manager import DbSessionManager
from .base_repository import BaseRepository


class ThingSettingsRepository(BaseRepository[ThingSettings], AbsThingSettingsRepository):
    """
    An implementation of SQLAlchemy-based storage
    of ThingSettingsRepository
    """
    def __init__(self, session_manager: DbSessionManager):
        """
        Constructor. Receives an instance of SessionManager
        to be used and saves a link to it to the internal
        variable.

        :param session_manager: an instance of SessionManager
               to be used for requesting SQLAlchemy Sessions
        """
        super().__init__(session_manager, stored_cls=ThingSettings)

    def select_by_integration(self, integration_id: str):  # -> Collection[ThingSettings]:
        """
        Selects and returns settings of all Things that
        belong to (are implemented in) the specified Integration

        :param integration_id: an identifier of Integration
               in interest
        :return: a collection of ThingSettings related to
                 the specified Integration
        """
        return self._session.query(self._stored_cls).filter_by(_integration=integration_id).all()

    def select_by_placement(self, placement_id: str):  # -> Collection[ThingSettings]:
        """
        Selects and returns settings of all Things that
        belong to (are placed in) the specified Placement

        :param placement_id: an identifier of Placement
               in interest
        :return: a collection of ThingSettings related to
                 the specified Placement
        """
        return self._session.query(self._stored_cls).filter_by(_placement_id=placement_id).all()

