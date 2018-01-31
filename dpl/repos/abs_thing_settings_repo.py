from .abs_repository import AbsRepository
from dpl.settings.thing_settings import ThingSettings


class AbsThingSettingsRepository(AbsRepository[ThingSettings]):
    """
    Pure abstract base implementation of Repository
    containing ThingSettings.

    Contains declarations of methods that must to be present
    in specific implementations of this repository
    """
    def select_by_integration(self, integration_id: str):  # -> Collection[ThingSettings]:
        """
        Selects and returns settings of all Things that
        belong to (are implemented in) the specified Integration

        :param integration_id: an identifier of Integration
               in interest
        :return: a collection of ThingSettings related to
                 the specified Integration
        """
        raise NotImplementedError()

    def select_by_placement(self, placement_id: str):  # -> Collection[ThingSettings]:
        """
        Selects and returns settings of all Things that
        belong to (are placed in) the specified Placement

        :param placement_id: an identifier of Placement
               in interest
        :return: a collection of ThingSettings related to
                 the specified Placement
        """
        raise NotImplementedError()
