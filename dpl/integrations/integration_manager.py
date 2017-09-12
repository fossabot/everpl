# Include standard modules
from typing import Dict, List, ValuesView
import logging
import importlib

# Include 3rd-party modules
# Include DPL modules
from dpl.connections import Connection
from dpl.things import Thing
from . import ConnectionFactory, ConnectionRegistry, ThingFactory, ThingRegistry

# Get logger:
LOGGER = logging.getLogger(__name__)


# FIXME: CC11: Consider splitting of IntegrationManager to ThingManager and ConnectionManager
# FIXME: CC12: Consider splitting of Managers to Repositories and Loaders
class IntegrationManager(object):
    """
    IntegrationManager is a class that is responsible for initiation, storage, fetching and deletion
    of Things and Connections.
    """
    def __init__(self):
        """
        Default constructor
        """
        self._connections = dict()  # type: Dict[str, Connection]
        self._things = dict()  # type: Dict[str, Thing]

    def init_integrations(self, integration_names: List[str]) -> None:
        """
        Load all enabled integrations from the specified list

        :param integration_names: a name of integrations to be loaded
        :return: None
        """
        for item in integration_names:
            try:
                importlib.import_module(name='.'+item, package="dpl.integrations")
            except ImportError as e:
                LOGGER.warning("Failed to load integration \"%s\": %s",
                               item, e)

    def init_connections(self, config: List[Dict]) -> None:
        """
        Initialize all connections by configuration data

        :param config: configuration data
        :return: None
        """
        for item in config:
            con_id = item["id"]
            integration_name = item["integration"]
            con_type = item["con_type"]
            con_params = item["con_params"]  # type: dict

            assert isinstance(con_params, dict)

            factory = ConnectionRegistry.resolve_factory(  # type: ConnectionFactory
                connection_type=con_type,
                default=None
            )

            if factory is None:
                LOGGER.warning(
                    "Failed to create connection \"%s\". Is integration \"%s\" enabled?",
                    con_id, integration_name
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
            thing_integration = item["integration"]
            thing_type = item["type"]
            thing_friendly_name = item.get("friendly_name", None)
            thing_placement = item["placement"]
            con_id = item["con_id"]
            con_params = item["con_params"]

            factory = ThingRegistry.resolve_factory(  # type: ThingFactory
                integration_name=thing_integration,
                thing_type=thing_type,
                default=None
            )

            connection = self._connections.get(con_id, None)  # type: Connection

            if connection is None:
                LOGGER.warning(
                    "Failed to create thing \"%s\": Connection \"%s\" is not available",
                    thing_id, con_id
                )

                continue

            if factory is None:
                LOGGER.warning(
                    "Failed to create thing \"%s\". Is integration \"%s\" enabled?",
                    thing_id, thing_integration
                )

                continue

            thing_instance = factory.build(  # type: Thing
                con_instance=connection,
                con_params=con_params,
                metadata={
                    "friendly_name": thing_friendly_name,
                    "type": thing_type,
                    "id": thing_id,
                    "placement": thing_placement
                }
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

