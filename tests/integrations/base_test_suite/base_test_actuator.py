# Include standard modules
import unittest
from unittest import mock
import time
import uuid

# Include 3rd-party modules
# Include DPL modules
from dpl.integrations.base_things import AbsActuator
from dpl.connections import Connection


class BaseTestActuator(unittest.TestCase):
    """
    A set of generic tests for Actuator interface implementations.
    """
    time_delta = 2
    base_commands = ('activate', 'deactivate', 'toggle')

    @classmethod
    def build_connection_mock(cls, *args, **kwargs) -> Connection:
        """
        Builds a MOCK instance of Connection that must be used
        in Unit Under Test instance.

        Must be overridden in derived classes.

        Example of implementation:
        >>> return mock.Mock(spec_set=Connection)

        :param args: position arguments of construction
        :param kwargs: keyword arguments of construction
        :return: an instance of Connection Mock
        """
        raise NotImplementedError

    @classmethod
    def build_uut(cls, *args, **kwargs) -> AbsActuator:
        """
        Builds Unit Under Test (uut) - an instance of Actuator to be tested.

        Must be overridden in derived classes.

        :param args: position arguments of construction
        :param kwargs: keyword arguments of construction
        :return: an instance of Actuator
        """
        raise NotImplementedError

    def setUp(self):
        # Build a mock of connection needed
        self.connection_mock = self.build_connection_mock()
        self.con_params = {'prefix': 'test'}
        self.metadata = {}

        # Build an instance of Actuator to be tested
        self.uut = self.build_uut(
            domain_id=uuid.uuid4().hex,
            con_instance=self.connection_mock,
            con_params=self.con_params,
            metadata=self.metadata
        )

        self.uut.enable()

    def tearDown(self):
        del self.uut
        del self.connection_mock
        del self.con_params
        del self.metadata

    def test_init(self):
        uut = self.build_uut(
            domain_id=uuid.uuid4().hex,
            con_instance=self.connection_mock,
            con_params=self.con_params,
            metadata=self.metadata
        )

        init_time = time.time()

        self.assertIsNot(uut.metadata, self.metadata)  # metadata must be copied, not linked to initial param
        self.assertEqual(uut.metadata, self.metadata)  # the copy of metadata must be identical to initial param

        # check that updates in original metadata don't affect the value of
        # Thing metadata field
        self.metadata["new_key"] = "new_value"
        self.assertNotEqual(uut.metadata, self.metadata)

        # default state of thing just after construction is unknown
        self.assertEqual(uut.state, uut.States.unknown)
        self.assertFalse(uut.is_active)

        # default value of last_updated field is equal to Thing init time
        self.assertAlmostEqual(
            uut.last_updated,
            init_time,
            self.time_delta
        )

        # Thing is disabled by default
        self.assertFalse(uut.is_enabled)
        # ... and thus is unavailable for communication by default
        self.assertFalse(uut.is_available)

    def test_enable(self):
        uut = self.build_uut(
            domain_id=uuid.uuid4().hex,
            con_instance=self.connection_mock,
            con_params=self.con_params,
            metadata=self.metadata
        )

        uut.enable()
        update_time = time.time()

        self.assertTrue(uut.is_enabled)
        self.assertAlmostEqual(
            uut.last_updated,
            update_time,
            self.time_delta
        )

    def test_disable(self):
        self.uut.disable()
        update_time = time.time()

        self.assertFalse(self.uut.is_enabled)
        self.assertFalse(self.uut.is_available)
        self.assertAlmostEqual(
            self.uut.last_updated,
            update_time,
            self.time_delta
        )

    def test_command_list(self):
        commands = self.base_commands

        for cmd in commands:
            self.assertIn(cmd, self.uut.commands)

    def test_activate(self):
        self.uut.activate()

        update_time = time.time()

        self.assertAlmostEqual(
            self.uut.last_updated,
            update_time,
            self.time_delta
        )

        self.assertTrue(self.uut.is_active)

    def test_deactivate(self):
        self.uut.deactivate()

        update_time = time.time()

        self.assertAlmostEqual(
            self.uut.last_updated,
            update_time,
            self.time_delta
        )

        self.assertFalse(self.uut.is_active)

    def test_execute_call_command_methods(self):
        args = ('one', 'two', 'three')
        kwargs = {"key1": "value1", "key2": "value2"}

        for cmd in self.uut.commands:
            with mock.patch.object(target=type(self.uut), attribute=cmd) as method_mock:
                self.uut.execute(cmd, *args, **kwargs)

                method_mock.assert_called_once_with(*args, **kwargs)

    def test_execute_unlisted_command(self):
        unknown_command = 'fchgmjbnkmlkljh'

        assert unknown_command not in self.uut.commands

        with self.assertRaises(ValueError):
            self.uut.execute(command=unknown_command)

    def test_call_non_command_method_as_command(self):
        cmd = 'enable'

        with self.assertRaises(ValueError):
            self.uut.execute(command=cmd)

    def test_toggle_fails_in_disabled_state(self):
        self.uut.disable()

        assert not self.uut.is_available

        with self.assertRaises(RuntimeError):
            self.uut.toggle()

    def test_all_commands_fails_in_disabled_state(self):
        self.uut.disable()

        assert not self.uut.is_available

        for cmd in self.uut.commands:
            with self.assertRaises(RuntimeError):
                self.uut.execute(cmd)

    def test_disable_preserves_state(self):
        self.uut.activate()
        state = self.uut.state

        self.uut.disable()

        assert not self.uut.is_available

        self.assertEqual(self.uut.state, state)

if __name__ == '__main__':
    unittest.main()
