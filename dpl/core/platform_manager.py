# Include standard modules
from typing import Dict, List

# Include 3rd-party modules
# Include DPL modules
from dpl.connections import Connection, ConnectionRegistry
from dpl.things import Thing, ThingRegistry


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

    def init_connections(self, config: List[Dict]) -> None:
        """
        Initialize all connections by configuration data
        :param config: configuration data
        :return: None
        """
        raise NotImplementedError

    def init_things(self, config: List[Dict]) -> None:
        """
        Initialize all things by configuration data
        :param config: configuration data
        :return: None
        """
        raise NotImplementedError

    def fetch_all_things(self):
        """
        Fetch a collection of all things
        :return: a collection of all things (type: ????)
        """
        raise NotImplementedError

    def fetch_thing(self, thing_id: str) -> Thing:
        """
        Fetch an instance of Thing by its ID
        :param thing_id: an ID of Thing to be fetched
        :return: an instance of Thing
        """
        raise NotImplementedError

    def enable_all_things(self) -> None:
        """
        Call Thing.enable method on all instances of things
        :return: None
        """
        raise NotImplementedError

    def disable_all_things(self) -> None:
        """
        Call Thing.enable method on all instances of things
        :return: None
        """
        raise NotImplementedError

