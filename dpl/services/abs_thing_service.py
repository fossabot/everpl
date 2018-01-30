from typing import Optional, Mapping, Any

from dpl.model.domain_id import TDomainId
from dpl.dtos.thing_dto import ThingDto
from .service_exceptions import ServiceEntityResolutionError, ServiceTypeError
from .abs_entity_service import AbsEntityService


class AbsThingService(AbsEntityService[ThingDto]):
    """
    A base class for all ThingService implementations
    """
    def create_thing(self, *args, **kwargs) -> None:
        """
        FIXME: METHOD SIGNATURE IS NOT YET DEFINED
        FIXME: !!! DEFINE METHOD SIGNATURE AND PREPARE A RELATED DOCUMENTATION !!!

        :param args: !!! NOT YET DEFINED !!!!
        :param kwargs: !!! NOT YET DEFINED !!!!
        :return:
        """
        raise NotImplementedError()

    def select_by_placement(self, placement_id: Optional[TDomainId]):  # -> Collection[ThingDto]:
        """
        Selects all Things that are physically present in the
        specified Placement

        :param placement_id: an identifier of the Placement
               of interest; or None (null) to fetch all Things
               that are not assigned to any Placement yet
        :return: a collection of Things that are placed in the
                 specified Placement
        """
        raise NotImplementedError()

    def send_command(self, to_actuator_id: TDomainId, command: str, command_args: Mapping[str, Any]) -> None:
        """
        Allows to send a command to Actuator or any other Thing
        which has an 'execute' method implemented.

        Internal logic is the following:

        - get an object by the specified ID;
        - check is this object has an 'execute' method;
        - check that the method signature is compatible;
        - check if the command is in a list allowed commands;
        - send a command to a Thing for execution;
        - raise an error if something gone wrong.

        :param to_actuator_id: an identifier of Things that is
               wanted to execute the specified command
        :param command: a name of a command to be executed
        :param command_args: additional command arguments to be
               passed to Thing for execution
        :return: None
        :raises ServiceEntityResolutionError: if the object with
                the specified ID can't be found
        :raises ServiceTypeError: if a thing with the specified
                identifier is not an instance of Actuator, doesn't
                implement 'execute' method and thus can't be used
                in this context
        """
        raise NotImplementedError()

    def change_property(self, thing_id: TDomainId, property_name: str, new_value: Any) -> None:
        """
        WARNING: THIS METHOD IS A SUBJECT TO BE CHANGED OR REMOVED

        FIXME: DOCUMENT OR REMOVE THIS METHOD

        :param thing_id:
        :param property_name:
        :param new_value:
        :return:
        """
        raise NotImplementedError()

    def enable(self, thing_id: TDomainId) -> None:
        """
        WARNING: THIS METHOD IS A SUBJECT TO BE CHANGED OR REMOVED

        FIXME: DOCUMENT OR REMOVE THIS METHOD

        :param thing_id:
        :return:
        """
        raise NotImplementedError()

    def disable(self, thing_id: TDomainId) -> None:
        """
        WARNING: THIS METHOD IS A SUBJECT TO BE CHANGED OR REMOVED

        FIXME: DOCUMENT OR REMOVE THIS METHOD

        :param thing_id:
        :return:
        """
        raise NotImplementedError()

    def get_settings(self, thing_id: TDomainId):  # ThingSettingsDto
        """
        WARNING: THIS METHOD IS A SUBJECT TO BE CHANGED OR REMOVED

        FIXME: DOCUMENT OR REMOVE THIS METHOD

        :param thing_id:
        :return:
        """
        raise NotImplementedError()

    def set_settings(self, thing_id: TDomainId, new_settings):
        """
        WARNING: THIS METHOD IS A SUBJECT TO BE CHANGED OR REMOVED

        FIXME: DOCUMENT OR REMOVE THIS METHOD

        :param thing_id:
        :param new_settings: # ThingSettingsDto
        :return:
        """
        raise NotImplementedError()
