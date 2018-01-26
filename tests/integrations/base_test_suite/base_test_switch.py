# Include standard modules
import unittest
import time

# Include 3rd-party modules
# Include DPL modules

# Include base tests for Actuator interface
from .base_test_actuator import BaseTestActuator


class BaseTestSwitch(BaseTestActuator):
    """
    A set of generic tests for Switch interface implementations.

    Calls all tests for Actuator interface implementations and
    adds some new Switch-related tests.
    """
    switch_specific_commands = ('on', 'off')

    def test_activate(self):
        super().test_activate()

        self.assertEqual(self.uut.state, self.uut.state.on)

    def test_deactivate(self):
        super().test_deactivate()

        self.assertEqual(self.uut.state, self.uut.state.off)

    def test_command_list(self):
        super().test_command_list()

        for cmd in self.switch_specific_commands:
            self.assertIn(cmd, self.uut.commands)

    def test_on(self):
        self.uut.on()

        update_time = time.time()

        self.assertAlmostEqual(
            self.uut.last_updated,
            update_time,
            self.time_delta
        )

        self.assertEqual(self.uut.state, self.uut.state.on)

    def test_off(self):
        self.uut.off()

        update_time = time.time()

        self.assertAlmostEqual(
            self.uut.last_updated,
            update_time,
            self.time_delta
        )

        self.assertEqual(self.uut.state, self.uut.state.off)

    def test_toggle_from_unknown(self):
        assert self.uut.state == self.uut.state.unknown

        self.uut.toggle()

        update_time = time.time()

        self.assertAlmostEqual(
            self.uut.last_updated,
            update_time,
            self.time_delta
        )

        self.assertEqual(self.uut.state, self.uut.state.on)

    def test_toggle_from_off(self):
        self.uut.off()

        self.uut.toggle()

        update_time = time.time()

        self.assertAlmostEqual(
            self.uut.last_updated,
            update_time,
            self.time_delta
        )

        self.assertEqual(self.uut.state, self.uut.state.on)

    def test_toggle_from_on(self):
        self.uut.on()

        self.uut.toggle()

        update_time = time.time()

        self.assertAlmostEqual(
            self.uut.last_updated,
            update_time,
            self.time_delta
        )

        self.assertEqual(self.uut.state, self.uut.state.off)

    # FIXME: CC21: Add tests for Actuator.state and Actuator is_active
    # field correlations

    def test_disable_preserves_state(self):
        self.uut.on()
        self.uut.disable()

        assert not self.uut.is_available

        self.assertEqual(self.uut.state, self.uut.state.on)

if __name__ == '__main__':
    unittest.main()
