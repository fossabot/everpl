# Include standard modules
import time

# Include 3rd-party modules
# Include DPL modules
from dpl.things import Player, ThingFactory, ThingRegistry
from . import DummyConnection


class DummyPlayer(Player):
    """
    A reference implementation of Player
    """
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

    @property
    def state(self) -> Player.States:
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

    def play(self, song_name: str) -> None:
        """
        Starts playing and switches the object to the 'playing' state. Additional parameters
        like track name or URL can be provided.
        :param song_name: song name to be played (or URL, or ID, or playlist position, etc.)
        :return: None
        """
        self._check_is_available()
        self._con_instance.print(self._print_prefix, "Player is playing {0}".format(song_name))
        self._state = self.States.playing

    def stop(self) -> None:
        """
        Stops playing and switches the object to the 'stopped' state.
        :return: None
        """
        self._check_is_available()
        self._con_instance.print(self._print_prefix, "Player is stopped")
        self._state = self.States.stopped

    def pause(self) -> None:
        """
        Pause playing and switches the object to the 'paused' state.
        :return: None
        """
        self._check_is_available()
        self._con_instance.print(self._print_prefix, "Player is paused")
        self._state = self.States.paused


class DummyPlayerFactory(ThingFactory):
    """
    DummyPlayerFactory is a class that is responsible for building of DummyPlayers
    """
    @staticmethod
    def build(*args, **kwargs) -> DummyPlayer:
        return DummyPlayer(*args, **kwargs)


ThingRegistry.register_factory(
    platform_name="dummy",
    thing_type="player",
    factory=DummyPlayerFactory()
)
