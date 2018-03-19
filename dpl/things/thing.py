# Include standard modules
import time
from copy import deepcopy
from types import MappingProxyType
from collections import Mapping

# Include 3rd-party modules
# Include DPL modules
from dpl.model.domain_id import TDomainId
from dpl.model.base_entity import BaseEntity
from dpl.connections import Connection
from dpl.things.capabilities.enabled import Enabled
from dpl.things.capabilities.available import Available
from dpl.things.capabilities.last_updated import LastUpdated


class Thing(BaseEntity, Enabled, Available, LastUpdated):
    """
    Thing is a base class for all connected devices in the system.

    Every implementation of Thing is an abstraction of real-life objects,
    devices, items, things that uses some specific protocol (connection) and
    can communicate with the system in any way.

    Specific implementations of things are grouped into 'integrations'.

    Every thing implementation must guarantee that:
    
    - a current state of thing is cached in internal buffer;
    - a current state of thing is always updated and corresponds to the current
      state of real object at the moment;
    - connection lost is indicated in specific property;
    - if connection is lost then the last known state of the object must be
      displayed in the corresponding property;
    - every implementation of a thing must notify all subscribers about the
      changes of thing state and connection state;
    - each thing has and additional 'is_available' property;
    - each thing can be 'enabled' and 'disabled';
    - 'disabled' thing doesn't update its state and doesn't try to support
      underlying connection alive;
    - 'enabled' thing tries to keep thing state updated;
    - 'is_available' property indicates that a communication with this thing
      can be performed;
    - 'is_available' is True **only** if thing is enabled **and** connection is
      not lost;
    - additional (optional) information about the object can be placed in
      so-called 'metadata';
    - usually the following metadata is saved: thing ID, user-friendly name,
      thing placement (position) information and some description.

    Derived classes are allowed to define additional methods and properties
    like 'current_track', 'play' and 'stop' for player. Or 'on'/'off' for
    lighting, etc.
    """

    def __init__(
            self, domain_id: TDomainId,
            con_instance: Connection, con_params: dict,
            metadata: dict = None
    ):
        """
        Constructor of a Thing. Receives an instance of Connection and some
        specific parameters to use it properly. Also can receive some metadata
        to be stored like object placement, description or user-friendly name.

        :param domain_id: a unique identifier of this Thing
        :param con_instance: an instance of connection to be used
        :param con_params: parameters to access connection
        :param metadata: metadata to be stored
        """
        super().__init__(domain_id)

        self._con_instance = con_instance
        self._con_params = con_params
        self._metadata = deepcopy(metadata)
        self._last_updated = time.time()
        self._is_enabled = False

    @property
    def metadata(self) -> Mapping:
        """
        Returns a stored metadata (read-only view of it)

        :return: metadata of objects
        """
        return MappingProxyType(self._metadata)

    @property
    def is_enabled(self) -> bool:
        """
        Indicates if the Thing is marked as enabled and it is allowed to
        communicate with.

        :return: True if communication is allowed, False otherwise
        """
        return self._is_enabled

    @property
    def last_updated(self) -> float:
        """
        Returns a timestamp of the last thing state update

        :return: float, UNIX time
        """
        return self._last_updated

    def _check_is_available(self) -> None:
        """
        Checks if this thing is available and raises and exception otherwise

        :return: None
        """
        # FIXME: CC40: Define a more specific exception for such situations
        if not self.is_available:
            raise RuntimeError("This thing is unavailable and can't be used at this time")

