class OnOff(object):
    """
    On/Off devices are devices that can be either powered “on” or “off”.
    The current state of those devices can be determined by the value of
    the is_power_on field.

    Actuator On/Off devices are able to be turned on and off with the on and
    off commands correspondingly. Actuator On/Off devices are MUST to provide
    ``on`` and ``off`` commands. And usually can be toggled between two states
    with a ``toggle`` command.

    If the device provides both on_off and is_active capabilities, then the
    on state is usually mapped to true value of is_active field and off state
    is mapped to false. on command is also mapped to the activate and off
    command is mapped to the deactivate command.
    """
    _capability_name = 'on_off'

    @property
    def is_powered_on(self) -> bool:
        """
        Indicates if this device powered on or not

        :return: True if this device is powered on, False otherwise.
        """
        raise NotImplementedError()
