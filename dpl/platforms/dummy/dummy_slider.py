# Include standard modules
import time

# Include 3rd-party modules
# Include DPL modules
from dpl.things import Slider
from . import DummyConnection


class DummySlider(Slider):
    """
    A reference implementation of slider
    """
    __SWITCH_DELAY = 1  # second

    def __init__(self, con_instance: DummyConnection, con_params: dict, metadata: dict):
        """
        Constructor. Receives an instance of DummyConnection and a prefix to be printed
        in con_params.
        :param con_instance: an instance of connection to be used
        :param con_params: a dict which contains connection access params
        :param metadata: some additional data that will be saved to 'metadata' property
        """
        super().__init__(con_instance, con_params, metadata)

        key_name = "prefix"

        try:
            self._print_prefix = con_params[key_name]
        except KeyError:
            raise ValueError("Invalid connection params passed: {0} parameter is missing".format(key_name))

        self._con_instance = con_instance
        self._is_enabled = True
        self._state = self.States.unknown
        self._last_updated = time.time()

    @property
    def state(self) -> Slider.States:
        """
        Return a current state of the Thing
        :return: an instance of self.State
        """
        return self._state

    @property
    def is_available(self) -> bool:
        """
        Availability of thing for usage and communication
        :return: True if Thing is available, False otherwise
        """
        return self._is_enabled  # and self._connection.is_connected

    @property
    def last_updated(self) -> float:
        """
        Returns a timestamp of the last thing state update
        :return: float, UNIX time
        """
        return self._last_updated

    def disable(self) -> None:
        """
        Forbid any activity and communication with physical object.
        Underlying connection can be closed, physical device performs
        everything on its own. Devices are allowed to switch to standby
        or power-saving mode. Thing 'state' property reflects only last
        known state of the physical object.
        :return: None
        """
        self._is_enabled = False

    def enable(self) -> None:
        """
        Allows communication with a physical object. Initiates a process
        of establishing connection to the physical device. Makes physical
        device to "wake up", to start receiving commands and sending of data.
        :return: None
        """
        self._is_enabled = True

    def open(self) -> None:
        """
        Switches an object to the 'opening' and then 'opened' state if its current state
        is 'undefined', 'closed' or 'closing'. Command must be ignored otherwise.
        :return: None
        """
        self._check_is_available()

        if self._state == self.States.opening or self._state == self.States.opened:
            pass
        else:
            self._con_instance.print(self._print_prefix, "Switch is opening...")
            self._state = self.States.opening

            time.sleep(self.__SWITCH_DELAY)

            self._con_instance.print(self._print_prefix, "Switch is opened")
            self._state = self.States.opened

    def close(self) -> None:
        """
        Switches an object to the 'closing' and then 'closed' state if its current state
        is 'undefined', 'opened' or 'opening'. Command must be ignored otherwise.
        :return: None
        """
        self._check_is_available()

        if self._state == self.States.closing or self._state == self.States.closed:
            pass
        else:
            self._con_instance.print(self._print_prefix, "Switch is closing...")
            self._state = self.States.closing

            time.sleep(self.__SWITCH_DELAY)

            self._con_instance.print(self._print_prefix, "Switch is closed")
            self._state = self.States.closed
