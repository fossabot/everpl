# Include standard modules
import unittest
from unittest import mock

# Include 3rd-party modules

# Include DPL modules
from dpl.integrations.connection_registry import \
    ConnectionFactory, ConnectionRegistry


class TestConnectionRegistry(unittest.TestCase):
    test_connection_type = "test_type"

    def setUp(self):
        self.registry = ConnectionRegistry()
        self.factory = mock.Mock(spec_set=ConnectionFactory)

    def tearDown(self):
        del self.registry
        del self.factory

    def test_resolve_unregistered(self):
        result = self.registry.resolve_factory(
            self.test_connection_type
        )

        self.assertEqual(result, None)

    def test_register_factory(self):
        self.registry.register_factory(
            self.test_connection_type,
            self.factory
        )

        result = self.registry.resolve_factory(
            self.test_connection_type
        )

        self.assertEqual(result, self.factory)

    def test_remove_factory(self):
        self.registry.register_factory(
            self.test_connection_type,
            self.factory
        )

        result = self.registry.resolve_factory(
            self.test_connection_type
        )

        self.assertEqual(result, self.factory)

        self.registry.remove_factory(
            self.test_connection_type
        )

        result = self.registry.resolve_factory(
            self.test_connection_type
        )

        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
