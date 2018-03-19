class Enabled(object):
    """
    Things with Enabled capability can be enabled or disabled.

    In 'disabled' state object becomes unavailable for any
    communication and is allowed to disconnect, terminate current
    communication session or turn off completely.

    In 'enabled' state everpl will try to support connection
    available without any interrupts. If connection with a device
    will be lost by some reason that everpl will try to recover
    it as soon as possible.
    """

    @property
    def is_enabled(self) -> bool:
        """
        Indicates if the Thing is marked as enabled and it is allowed to
        communicate with.

        :return: True if communication is allowed, False otherwise
        """
        raise NotImplementedError()

    def disable(self) -> None:
        """
        Forbid any activity and communication with physical object.
        Underlying connection can be closed, physical device performs
        everything on its own. Devices are allowed to switch to standby
        or power-saving mode. Thing 'state' property reflects only last
        known state of the physical object.

        :return: None
        """
        raise NotImplementedError()

    def enable(self) -> None:
        """
        Allows communication with a physical object. Initiates a process
        of establishing connection to the physical device. Makes physical
        device to "wake up", to start receiving commands and sending of data.

        :return: None
        """
        raise NotImplementedError()
