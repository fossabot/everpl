# Include standard modules
import unittest
from unittest import mock

# Include 3rd-party modules

# Include DPL modules
from dpl.integrations.thing_registry import \
    ThingFactory, ThingRegistry


class TestConnectionRegistry(unittest.TestCase):
    test_integration_name = "test_integration"
    test_thing_type = "nobody_cares"

    def setUp(self):
        self.registry = ThingRegistry()
        self.factory = mock.Mock(spec_set=ThingFactory)

    def tearDown(self):
        del self.registry
        del self.factory

    def test_resolve_unregistered(self):
        result = self.registry.resolve_factory(
            self.test_thing_type,
            self.test_integration_name
        )

        self.assertIs(result, None)

    def test_register_factory(self):
        self.registry.register_factory(
            self.test_integration_name,
            self.test_thing_type,
            self.factory
        )

        result = self.registry.resolve_factory(
            self.test_integration_name,
            self.test_thing_type
        )

        self.assertIs(result, self.factory)

    def test_remove_factory(self):
        self.registry.register_factory(
            self.test_integration_name,
            self.test_thing_type,
            self.factory
        )

        result = self.registry.resolve_factory(
            self.test_integration_name,
            self.test_thing_type
        )

        self.assertIs(result, self.factory)

        self.registry.remove_factory(
            self.test_integration_name,
            self.test_thing_type
        )

        result = self.registry.resolve_factory(
            self.test_integration_name,
            self.test_thing_type
        )

        self.assertIs(result, None)


if __name__ == '__main__':
    unittest.main()
