import logging
import importlib

from typing import Iterable, Mapping

from dpl.connections.connection import Connection
from dpl.things.thing import Thing

from dpl.repos.abs_connection_repository import AbsConnectionRepository
from dpl.repos.abs_thing_repository import AbsThingRepository

from .connection_registry import ConnectionRegistry
from .connection_factory import ConnectionFactory

from .thing_registry import ThingRegistry
from .thing_factory import ThingFactory

LOGGER = logging.getLogger(__name__)


class BindingBootstrapper(object):
    """
    BindingBootstrapper is responsible for initialization
    of all integrations and for instantiation of Things
    and Connections based on the configuration files

    WARNING: It's likely that this class will be removed
             in the next release and replaced by some other
             class
    """
    def __init__(self, connection_repo: AbsConnectionRepository, thing_repo: AbsThingRepository):
        """
        Constructor. Copies links to ConnectionRepository and
        ThingRepository to be initialized to the internal storage

        :param connection_repo: an instance of ConnectionRepository
               to be initialized
        :param thing_repo: an instance of ThingRepository
               to be initialized
        """
        self._connections = connection_repo
        self._things = thing_repo

    @staticmethod
    def init_integrations(integration_names: Iterable[str]) -> None:
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

    def init_connections(self, config: Iterable[Mapping]) -> None:
        """
        Initialize all connections by configuration data

        :param config: configuration data
        :return: None
        """
        for item in config:
            con_id = item["id"]
            integration_name = item["integration"]
            con_type = item["con_type"]
            con_params = item["con_params"]  # type: Mapping

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
                domain_id=con_id, **con_params
            )

            self._connections.add(con_instance)

    def init_things(self, config: Iterable[Mapping]) -> None:
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

            connection = self._connections.load(con_id)  # type: Connection

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
                domain_id=thing_id,
                con_instance=connection,
                con_params=con_params,
                metadata={
                    "friendly_name": thing_friendly_name,
                    "type": thing_type,
                    "placement": thing_placement
                }
            )

            self._things.add(thing_instance)
