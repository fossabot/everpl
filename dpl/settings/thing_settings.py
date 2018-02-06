from typing import Any, Optional, Mapping
from types import MappingProxyType

from dpl.model.base_entity import BaseEntity
from dpl.model.domain_id import TDomainId


class ThingSettings(BaseEntity):
    """
    ThingSettings is a some entity which is responsible
    for storage of all data needed to initialize a Thing
    like its friendly_name, unique identifier, placement,
    used connection and parameters used to access a physical
    device using the specified connection
    """
    def __init__(
            self, domain_id: TDomainId,
            integration: str, thing_type: str,
            con_id: TDomainId, con_params: Mapping[str, Any],
            friendly_name: Optional[str],
            placement_id: Optional[TDomainId]
    ):
        """
        Constructor. Receives all data needed to store in
        an instance of ThingSettings

        :param domain_id: an unique identifier of the Thing
               that will be created by this settings
        :param integration: string, an identifier of Integration
               that provides implementation of this Thing
        :param thing_type: string, an identifier of Thing type
               provided by Integration
        :param con_id: a unique identifier of Connection to be
               used by this Thing
        :param con_params: some parameters used to access the
               specified Connection (like GPIO pin numbers)
        :param friendly_name: string or None (null), some
               human-friendly name or title of this Thing
        :param placement_id: a unique identifier of Placement
               where this Thing is physically located; can be
               None if the specified Thing is not yet assigned
               to any Placement
        """
        super().__init__(domain_id)

        self._integration = integration
        self._thing_type = thing_type
        self._con_id = con_id
        self._con_params = con_params
        self._friendly_name = friendly_name
        self._placement_id = placement_id

    @property
    def integration(self) -> str:
        """
        Returns an identifier of Integration that provides
        implementation of this Thing

        :return: an identifier of Integration that provides
                 implementation of this Thing
        """
        return self._integration

    @property
    def thing_type(self) -> str:
        """
        Returns an identifier of Thing type provided by
        Integration

        :return: an identifier of Thing type provided by
                 Integration
        """
        return self._thing_type

    @property
    def connection_id(self) -> TDomainId:
        """
        Returns a unique identifier of Connection to be
        used by this Thing

        :return: a unique identifier of Connection to be
                 used by this Thing
        """
        return self._con_id

    @property
    def connection_params(self) -> Mapping[str, Any]:
        """
        Returns some parameters used to access the specified
        Connection (like GPIO pin numbers)

        :return: some parameters used to access the specified
                 Connection (like GPIO pin numbers)
        """
        return MappingProxyType(self._con_params)

    @property
    def friendly_name(self) -> Optional[str]:
        """
        Returns string or None (null), some human-friendly
        name or title of this Thing

        :return: some human-friendly name or title of this Thing
        """
        return self._friendly_name

    @friendly_name.setter
    def friendly_name(self, new_name: Optional[str]) -> None:
        """
        Allows to set a new human-friendly name for this Thing

        :param new_name: new name to be set or None to unset
               the current name value
        :return: None
        """
        self._friendly_name = new_name

    @property
    def placement_id(self) -> Optional[TDomainId]:
        """
        Returns a unique identifier of Placement where this
        Thing is physically located; can be None if the
        specified Thing is not yet assigned to any Placement

        :return: a unique identifier of Placement where this
                 Thing is physically located or None if the
                 specified Thing is not yet assigned to any
                 Placement
        """
        return self._placement_id

    @placement_id.setter
    def placement_id(self, new_placement: Optional[TDomainId]) -> None:
        """
        Allows to set a new Placement for this Thing

        :param new_placement: an identifier of new Placement to
               be set or None to unset the current value
        :return: None
        """
        self._placement_id = new_placement
