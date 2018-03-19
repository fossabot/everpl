# Include standard modules
# Include 3rd-party modules

# Include DPL modules
from dpl.integrations.abs_switch import AbsSwitch
from dpl.integrations import ThingFactory, ThingRegistry
from dpl.model.domain_id import TDomainId

from .dummy_connection import DummyConnection


class DummySwitch(AbsSwitch):
    def __init__(
            self, domain_id: TDomainId,
            con_instance: DummyConnection, con_params: dict,
            metadata: dict
    ):
        """
        Constructor. Receives an instance of DummyConnection and a prefix to
        be printed in con_params.

        :param domain_id: a unique identifier of this Thing
        :param con_instance: an instance of connection to be used
        :param con_params: a dict which contains connection access params
        :param metadata: some additional data that will be saved to 'metadata'
               property
        """
        super().__init__(domain_id, con_instance, con_params, metadata)

        key_name = "prefix"

        try:
            self._print_prefix = con_params[key_name]
        except KeyError:
            raise ValueError("Invalid connection params passed: "
                             "{0} parameter is missing".format(key_name))

        self._con_instance = con_instance

    @property
    def state(self) -> AbsSwitch.States:
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

    def on(self) -> None:
        """
        Switches an object to the 'on' state

        :return: None
        """
        self._check_is_available()
        self._con_instance.print(self._print_prefix, "Switch is turned on")
        self._state = self.States.on

    def off(self) -> None:
        """
        Switches an object to the 'off' state

        :return: None
        """
        self._check_is_available()
        self._con_instance.print(self._print_prefix, "Switch is turned off")
        self._state = self.States.off


class DummySwitchFactory(ThingFactory):
    """
    DummySliderFactory is a class that is responsible for building of
    DummySliders
    """
    @staticmethod
    def build(*args, **kwargs) -> DummySwitch:
        return DummySwitch(*args, **kwargs)


ThingRegistry.register_factory(
    integration_name="dummy",
    thing_type="switch",
    factory=DummySwitchFactory()
)
