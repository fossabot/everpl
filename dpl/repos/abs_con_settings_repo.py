from .abs_repository import AbsRepository
from dpl.settings.connection_settings import ConnectionSettings


class AbsConnectionSettingsRepository(AbsRepository[ConnectionSettings]):
    """
    Pure abstract base implementation of Repository
    containing ConnectionSettings.

    Contains declarations of methods that must to be present
    in specific implementations of this repository
    """
    def select_by_integration(self, integration_id: str):  # -> Collection[ConnectionSettings]:
        """
        Selects and returns settings of all Connections that
        belong to (are implemented in) the specified Integration

        :param integration_id: an identifier of Integration
               in interest
        :return: a collection of ConnectionSettings related to
                 the specified Integration
        """
        raise NotImplementedError()
