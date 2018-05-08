import weakref
from typing import Optional, Mapping, Any, Callable

from dpl.utils.observer import Observer
from dpl.model.domain_id import TDomainId
from dpl.things.thing import Thing
from dpl.integrations.abs_actuator import (
    AbsActuator, UnsupportedCommandError, UnacceptableCommandArgumentsError
)
from dpl.dtos.thing_dto import ThingDto
# noinspection PyUnresolvedReferences
from dpl.dtos.actuator_dto import ActuatorDto
from dpl.dtos.dto_builder import build_dto
from dpl.services.abs_thing_service import (
    AbsThingService,
    ServiceEntityResolutionError,
    ServiceTypeError,
    ServiceInvalidArgumentsError,
    ServiceUnsupportedCommandError
)

from dpl.repos.observable_repository import RepositoryEventType
from dpl.repos.abs_thing_repository import AbsThingRepository
from .base_observable_service import BaseObservableService, ServiceEventType


class RepoObserver(Observer[AbsThingRepository]):
    """
    A utility class objects of which will observe changes in
    ObservableRepository and emit events on each change
    """

    def __init__(self, callback: Callable):
        """
        Constructor. Receives a callback to be called if something will be
        changed in the repository

        :param callback: a callback to be called if something will be
               changed in the repository
        """
        self._callback = callback

    def update(self, source: AbsThingRepository, *args, **kwargs) -> None:
        """
        Method which redirects all the event data to the registered
        callback

        :param source: a source of the received event
        :param args: positional arguments to be redirected
        :param kwargs: keyword arguments to be redirected
        :return: None
        """
        self._callback(*args, **kwargs)


class ThingService(BaseObservableService[Thing, ThingDto], AbsThingService):
    """
    This is an implementation of a ThingService - a class
    that manages all Things in the system

    FIXME: Implement all methods of an abstract class
    """
    def __init__(self, thing_repo: AbsThingRepository):
        """
        Constructor. Receives an instance of ThingRepository
        which will be used to store all Things and fetch them

        WARNING: Additional params are possible to be added in
                 future !!!

        :param thing_repo: an instance of a ThingRepository
        """
        super().__init__()
        self._things = thing_repo
        self._things_observer = RepoObserver(self._handle_repository_update)
        self._things.subscribe(self._things_observer)
        self._weak_self = weakref.proxy(self)

    def _handle_repository_update(
            self, event_type: RepositoryEventType, object_id: TDomainId,
            object_ref: Thing
    ):
        """
        Utility method to convert events emitted by ThingRepository to events
        suitable to be passed in _notify called

        :param event_type: a type of the event emitted
        :param object_id: an identifier of a changed object
        :param object_ref: a reference to the changed object
        :return: None
        """
        service_event_type = ServiceEventType(event_type.value)

        if service_event_type is ServiceEventType.deleted:
            thing_dto = None
        else:
            thing_dto = build_dto(object_ref)

        self._notify(
            object_id=object_id,
            event_type=service_event_type,
            object_dto=thing_dto
        )

    def view(self, domain_id: TDomainId) -> ThingDto:
        """
        Fetch a DTO of stored object by the ID specified

        :param domain_id: id of object to be fetched
        :return: a DTO of stored object
        :raises ServiceResolutionError: if the entity with
                the specified ID can't be found
        """
        thing = self._things.load(domain_id)

        if thing is None:
            raise ServiceEntityResolutionError()

        return build_dto(thing)

    def view_all(self):  # -> Collection[ThingDto]:
        """
        Fetch a full list of DTOs of all stored objects

        :return: a collection of DTOs
        """
        return [
            build_dto(i) for i in self._things.load_all()
        ]

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
        # FIXME: Handle exceptions caused by resolution errors
        # FIXME: Handle exceptions caused by link breakages
        self._things.delete(domain_id)

    def select_by_placement(
            self, placement_id: Optional[TDomainId]
    ):  # -> Collection[ThingDto]:
        """
        Selects all Things that are physically present in the
        specified Placement

        :param placement_id: an identifier of the Placement
               of interest; or None (null) to fetch all Things
               that are not assigned to any Placement yet
        :return: a collection of Things that are placed in the
                 specified Placement
        """
        return [
            build_dto(i) for i in self._things.select_by_placement(placement_id)
        ]

    def send_command(
            self, to_actuator_id: TDomainId,
            command: str, command_args: Mapping[str, Any]
    ) -> None:
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
        :raises ServiceUnsupportedCommandError: if the specified
                command is not supported by this instance of Thing
        :raises ServiceUnsupportedCommandError:
        """
        thing = self._things.load(to_actuator_id)  # type: AbsActuator

        if thing is None:
            raise ServiceEntityResolutionError(
                "The instance of Thing with the specified ID "
                "can't be found: %s" % to_actuator_id
            )

        # FIXME: Check base types instead of a presence of method
        execute_method = getattr(thing, 'execute', None)
        if execute_method is None:
            raise ServiceTypeError(
                "The specified instance of Thing is not an Actuator "
                "and doesn't have a command execution capability: %s"
                % to_actuator_id
            )

        # FIXME: Handle validation and execution errors
        # FIXME: Ensure that such calls will be safe
        try:
            thing.execute(command, command_args)

        except UnacceptableCommandArgumentsError as e:
            raise ServiceInvalidArgumentsError() from e

        except UnsupportedCommandError as e:
            raise ServiceUnsupportedCommandError() from e

    def enable_all(self) -> None:
        """
        Enables all things. Calls 'enable' method on all instances
        of Thing that are present in the system

        :return: None
        """
        for t in self._things.load_all():
            t.enable()

    def disable_all(self) -> None:
        """
        Disables all things. Calls 'disable' method on all instances
        of Thing that are present in the system

        :return: None
        """
        for t in self._things.load_all():
            t.disable()
