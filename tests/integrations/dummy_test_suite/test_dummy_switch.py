# Include standard modules
import unittest
from unittest import mock
import time

# Include 3rd-party modules
# Include DPL modules
from dpl.integrations.dummy import DummyConnection
from dpl.integrations.dummy import DummySwitch

# TODO: Split common tests into generic TestCases


class TestDummySwitch(unittest.TestCase):
    time_delta = 2
    base_commands = ('activate', 'deactivate', 'toggle')

    def setUp(self):
        self.connection_mock = mock.Mock(spec_set=DummyConnection)
        self.con_params = {'prefix': 'test'}
        self.metadata = {}

        self.switch = DummySwitch(
            con_instance=self.connection_mock,
            con_params=self.con_params,
            metadata=self.metadata
        )

        self.switch.enable()

    def tearDown(self):
        del self.switch
        del self.connection_mock
        del self.con_params
        del self.metadata

    def test_init(self):
        switch = DummySwitch(
            con_instance=self.connection_mock,
            con_params=self.con_params,
            metadata=self.metadata
        )

        init_time = time.time()

        self.assertIsNot(switch.metadata, self.metadata)  # metadata must be copied, not linked to initial param
        self.assertEqual(switch.metadata, self.metadata)  # the copy of metadata must be identical to initial param

        # check that updates in original metadata don't affect the value of
        # Thing metadata field
        self.metadata["new_key"] = "new_value"
        self.assertNotEqual(switch.metadata, self.metadata)

        # default state of thing just after construction is unknown
        self.assertEqual(switch.state, switch.States.unknown)
        self.assertFalse(switch.is_active)

        # default value of last_updated field is equal to Thing init time
        self.assertAlmostEqual(
            switch.last_updated,
            init_time,
            self.time_delta
        )

        # Thing is disabled by default
        self.assertFalse(switch.is_enabled)
        # ... and thus is unavailable for communication by default
        self.assertFalse(switch.is_available)

    def test_enable(self):
        switch = DummySwitch(
            con_instance=self.connection_mock,
            con_params=self.con_params,
            metadata=self.metadata
        )

        switch.enable()
        update_time = time.time()

        self.assertTrue(switch.is_enabled)
        self.assertAlmostEqual(
            switch.last_updated,
            update_time,
            self.time_delta
        )

    def test_disable(self):
        self.switch.disable()
        update_time = time.time()

        self.assertFalse(self.switch.is_enabled)
        self.assertFalse(self.switch.is_available)
        self.assertAlmostEqual(
            self.switch.last_updated,
            update_time,
            self.time_delta
        )

    def test_command_list(self):
        commands = self.base_commands + ('on', 'off')

        self.assertSequenceEqual(self.switch.commands, commands)

    def test_activate(self):
        self.switch.activate()

        update_time = time.time()

        self.assertAlmostEqual(
            self.switch.last_updated,
            update_time,
            self.time_delta
        )

        self.assertTrue(self.switch.is_active)
        self.assertEqual(self.switch.state, self.switch.state.on)

    def test_deactivate(self):
        self.switch.deactivate()

        update_time = time.time()

        self.assertAlmostEqual(
            self.switch.last_updated,
            update_time,
            self.time_delta
        )

        self.assertFalse(self.switch.is_active)
        self.assertEqual(self.switch.state, self.switch.state.off)

    def test_on(self):
        self.switch.on()

        update_time = time.time()

        self.assertAlmostEqual(
            self.switch.last_updated,
            update_time,
            self.time_delta
        )

        self.assertEqual(self.switch.state, self.switch.state.on)

    def test_off(self):
        self.switch.off()

        update_time = time.time()

        self.assertAlmostEqual(
            self.switch.last_updated,
            update_time,
            self.time_delta
        )

        self.assertEqual(self.switch.state, self.switch.state.off)

    def test_toggle_from_unknown(self):
        assert self.switch.state == self.switch.state.unknown

        self.switch.toggle()

        update_time = time.time()

        self.assertAlmostEqual(
            self.switch.last_updated,
            update_time,
            self.time_delta
        )

        self.assertEqual(self.switch.state, self.switch.state.on)

    def test_toggle_from_off(self):
        self.switch.off()

        self.switch.toggle()

        update_time = time.time()

        self.assertAlmostEqual(
            self.switch.last_updated,
            update_time,
            self.time_delta
        )

        self.assertEqual(self.switch.state, self.switch.state.on)

    def test_toggle_from_on(self):
        self.switch.on()

        self.switch.toggle()

        update_time = time.time()

        self.assertAlmostEqual(
            self.switch.last_updated,
            update_time,
            self.time_delta
        )

        self.assertEqual(self.switch.state, self.switch.state.off)

    # FIXME: CC21: Add tests for state on is_active correlations

    def test_all_commands_has_methods(self):
        for cmd in self.switch.commands:
            result = getattr(self.switch, cmd, default=None)

            self.assertIsNotNone(result)

    def test_execute_call_command_methods(self):
        args = ('one', 'two', 'three')
        kwargs = {"key1": "value1", "key2": "value2"}

        for cmd in self.switch.commands:
            with mock.patch.object(target=DummySwitch, attribute=cmd) as method_mock:
                self.switch.execute(cmd, *args, **kwargs)

                method_mock.assert_called_once_with(*args, **kwargs)

    def test_execute_unlisted_command(self):
        unknown_command = 'fchgmjbnkmlkljh'

        with self.assertRaises(ValueError):
            self.switch.execute(command=unknown_command)

    def test_call_non_command_method_as_command(self):
        cmd = 'enable'

        with self.assertRaises(ValueError):
            self.switch.execute(command=cmd)

    def test_toggle_fails_in_disabled_state(self):
        self.switch.disable()

        assert not self.switch.is_available

        with self.assertRaises(RuntimeError):
            self.switch.toggle()

    def test_all_commands_fails_in_disabled_state(self):
        self.switch.disable()

        assert not self.switch.is_available

        for cmd in self.switch.commands:
            with self.assertRaises(RuntimeError):
                self.switch.execute(cmd)

    def test_disable_preserves_state(self):
        self.switch.on()
        self.switch.disable()

        assert not self.switch.is_available

        self.assertEqual(self.switch.state, self.switch.state.on)

if __name__ == '__main__':
    unittest.main()
