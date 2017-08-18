# Include standard modules
from enum import Enum

# Include 3rd-party modules
# Include DPL modules
from dpl.connections import Connection


class Thing(object):
    """
    Thing is a base class for all connected devices in the system.

    Every implementation of Thing is an abstraction of real-life objects, devices,
    items, things that uses some specific protocol (connection) and can communicate
    with the system in any way.

    Specific implementations of things are grouped into 'platforms'.

    Every thing implementation must guarantee that:
    - a current state of thing is cached in internal buffer;
    - a current state of thing is always updated and corresponds to the current
      state of real object at the moment;
    - connection lost is indicated in specific property;
    - if connection is lost then the last known state of the object must be displayed
      in corresponding property;
    - every implementation of a thing must notify all subscribers about the changes of
      thing state and connection state;
    - each thing has and additional 'is_available' property;
    - each thing can be 'enabled' and 'disabled';
    - 'disabled' thing doesn't update its state and doesn't try to support underlying
      connection alive;
    - 'enabled' thing tries to keep thing state updated;
    - 'is_available' property indicates that a communication with this thing can be
      performed;
    - 'is_available' is True **only** if thing is enabled **and** connection is not lost.

    Derived classes are allowed to define additional methods and properties like
    'current_track', 'play' and 'stop' for player. Or 'on'/'off' for lighting, etc.
    """

    class States(Enum):
        """
        Possible states of the thing. Must be overridden in derived classes
        """
        unknown = None

    def __init__(self, con_instance: Connection, con_params: dict, metadata: dict = None):
        """
        Constructor of a Thing. Receives an instance of Connection and some specific
        parameters to use it properly. Also can receive some metadata to be stored like
        object placement, description or user-friendly name.
        :param con_instance: an instance of connection to be used
        :param con_params: parameters to access connection
        :param metadata: metadata to be stored
        """
        self._con_instance = con_instance
        self._con_params = con_params
        self._metadata = metadata
        self._on_update = None
        self._on_avail_update = None

    @property
    def metadata(self) -> dict:
        """
        Returns a stored metadata
        :return: metadata of objects
        """
        return self._metadata

    @property
    def state(self) -> States:
        """
        Return a current state of the Thing
        :return: an instance of self.State
        """
        raise NotImplementedError

    @property
    def is_available(self) -> bool:
        """
        Availability of thing for usage and communication
        :return: True if Thing is available, False otherwise
        """
        raise NotImplementedError

    @property
    def last_updated(self) -> float:
        """
        Returns a timestamp of the last thing state update
        :return: float, UNIX time
        """
        raise NotImplementedError

    def disable(self) -> None:
        """
        Forbid any activity and communication with physical object.
        Underlying connection can be closed, physical device performs
        everything on its own. Devices are allowed to switch to standby
        or power-saving mode. Thing 'state' property reflects only last
        known state of the physical object.
        :return: None
        """
        raise NotImplementedError

    def enable(self) -> None:
        """
        Allows communication with a physical objects. Initiates a process
        of establishing connection to the physical device. Makes physical
        device to "wake up", to start receiving commands and sending of data.
        :return: None
        """
        raise NotImplementedError

