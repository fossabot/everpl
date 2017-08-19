# Include standard modules
from typing import Dict, List, ValuesView
import logging
import importlib

# Include 3rd-party modules
# Include DPL modules
from dpl.connections import Connection, ConnectionRegistry, ConnectionFactory
from dpl.things import Thing, ThingRegistry, ThingFactory
import dpl.platforms

# Get logger:
LOGGER = logging.getLogger(__name__)


# FIXME: CC11: Consider splitting of PlatformManager to ThingManager and ConnectionManager
# FIXME: CC12: Consider splitting of Managers to Repositories and Loaders
class PlatformManager(object):
    """
    PlatformManager is a class that is responsible for initiation, storage, fetching and deletion
    of Things and Connections.
    """
    def __init__(self):
        """
        Default constructor
        """
        self._connections = dict()  # type: Dict[str, Connection]
        self._things = dict()  # type: Dict[str, Thing]

    def init_platforms(self, platform_names: List[str]) -> None:
        """
        Load all enabled platforms from the specified list
        :param platform_names: a name of platforms to be loaded
        :return: None
        """
        for item in platform_names:
            importlib.import_module(name=item, package="dpl.platforms")

    def init_connections(self, config: List[Dict]) -> None:
        """
        Initialize all connections by configuration data
        :param config: configuration data
        :return: None
        """
        for item in config:
            con_id = item["id"]
            platform_name = item["platform"]
            con_type = item["con_type"]
            con_params = item["con_params"]  # type: dict

            assert isinstance(con_params, dict)

            factory = ConnectionRegistry.resolve_factory(  # type: ConnectionFactory
                connection_type=con_type,
                default=None
            )

            if factory is None:
                LOGGER.warning(
                    "Failed to create connection \"%s\". Is platform \"%s\" enabled?",
                    con_id, platform_name
                )

                continue

            con_instance = factory.build(  # type: Connection
                **con_params
            )

            self._connections[con_id] = con_instance

    def init_things(self, config: List[Dict]) -> None:
        """
        Initialize all things by configuration data
        :param config: configuration data
        :return: None
        """
        for item in config:
            thing_id = item["id"]
            thing_platform = item["platform"]
            thing_type = item["type"]
            thing_description = item["description"]
            con_id = item["con_id"]
            con_params = item["con_params"]

            factory = ThingRegistry.resolve_factory(  # type: ThingFactory
                platform_name=thing_platform,
                thing_type=thing_type,
                default=None
            )

            connection = self._connections.get(con_id, None)  # type: Connection

            if connection is None:
                LOGGER.warning(
                    "Failed to create thing \"%s\": Connection \"%s\" is not available",
                    thing_id, thing_platform
                )

                continue

            if factory is None:
                LOGGER.warning(
                    "Failed to create thing \"%s\". Is platform \"%s\" enabled?",
                    thing_id, thing_platform
                )

                continue

            thing_instance = factory.build(  # type: Thing
                con_instance=connection,
                con_params=con_params,
                metadata={"description": thing_description}
            )

            self._things[thing_id] = thing_instance

    def fetch_all_things(self) -> ValuesView[Thing]:
        """
        Fetch a collection of all things
        :return: a set-like object containing all things
        """
        return self._things.values()

    def fetch_thing(self, thing_id: str) -> Thing:
        """
        Fetch an instance of Thing by its ID
        :param thing_id: an ID of Thing to be fetched
        :return: an instance of Thing
        """
        return self._things[thing_id]

    def enable_all_things(self) -> None:
        """
        Call Thing.enable method on all instances of things
        :return: None
        """
        for thing in self._things.values():
            thing.enable()

    def disable_all_things(self) -> None:
        """
        Call Thing.enable method on all instances of things
        :return: None
        """
        for thing in self._things.values():
            thing.disable()

