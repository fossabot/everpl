"""
This is an example of test suite for platform-specific implementations
of Switch. Every such test must to run all tests related to the Switch
interface and all its parents. Also it's allowed to override base test
methods and add new ones for testing of platform-specific behaviour.
"""


# Include standard modules
import unittest
from unittest import mock

# Include 3rd-party modules
# Include DPL modules
from everpli_dummy import DummyConnection, DummySwitch


# Import base test case for all Switch interface implementations
from tests.integrations.base_test_suite import base_test_switch as base


class TestDummySwitch(base.BaseTestSwitch):
    @classmethod
    def build_uut(cls, *args, **kwargs) -> DummySwitch:
        # Redefine builder function - return a platform-specific
        # implementation of Switch
        return DummySwitch(*args, **kwargs)

    @classmethod
    def build_connection_mock(cls, *args, **kwargs) -> DummyConnection:
        # Redefine builder function - return a platform-specific
        # implementation of Connection
        return mock.Mock(spec_set=DummyConnection)

    # Everything else is handled by generic interface tests


if __name__ == '__main__':
    unittest.main()
