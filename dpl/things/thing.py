# Include standard modules
import time
from copy import deepcopy
from types import MappingProxyType
from typing import Mapping, Sequence
import weakref

from typing import Optional, Callable

# Include 3rd-party modules
# Include DPL modules
from dpl.model.domain_id import TDomainId
from dpl.model.base_entity import BaseEntity
from dpl.connections import Connection
from dpl.things.capabilities.is_enabled import IsEnabled
from dpl.things.capabilities.is_available import Available
from dpl.things.capabilities.last_updated import LastUpdated
from .capability_filler_meta import CapabilityFiller
from .update_callback import UpdateCallback


class Thing(BaseEntity, IsEnabled, Available, LastUpdated, UpdateCallback,
            metaclass=CapabilityFiller):
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
    # _capabilities field will be filled by the CapabilityFiller metaclass
    _capabilities = None   # type: Sequence[str]

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
        self._on_update = None

    @property
    def capabilities(self) -> Sequence[str]:  # -> Collection[str]:
        """
        Returns a list of Capabilities supported by this Thing

        :return: a collection of Capability names supported by
                 (implemented by) this Thing
        """
        return self._capabilities

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

    @property
    def on_update(self) -> Optional[Callable]:
        """
        Returns a callable that is currently registered to be called on each
        update of this object

        :return: a callable that is currently registered to be called on each
                 update of this object; or None if a callable wasn't set yet
        """
        return self._on_update

    @on_update.setter
    def on_update(self, callback: Optional[Callable]) -> None:
        """
        Allows to set a callable to be called on each update of this object.
        This callable must to accept a reference to the event source (i.e. to
        this object)

        :param callback: a new callback to be set or None to unset a callback
        :return: None
        """
        self._on_update = callback

    def _check_is_available(self) -> None:
        """
        Checks if this thing is available and raises and exception otherwise

        :return: None
        """
        # FIXME: CC40: Define a more specific exception for such situations
        if not self.is_available:
            raise RuntimeError("This thing is unavailable and can't be used at this time")

    def _apply_update(self) -> None:
        """
        A method to be called after EACH update to ANY of the Thing's field.
        Updates the value of last_updated field and calls a callback registered
        in on_update property

        :return: None
        """
        self._last_updated = time.time()

        if self._on_update:
            self._on_update(self)
