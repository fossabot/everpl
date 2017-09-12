# Include standard modules
from typing import Dict

# Include 3rd-party modules
# Include DPL modules
from . import ThingFactory


class ThingRegistry(object):
    """
    ThingFactory is a class that registers all things, implemented
    in specific integrations (dpl.integrations module), and returns a corresponding
    ThingFactory for building of instance of this thing.
    """
    # contains references to all factories:
    __registry = dict()  # type: Dict['str', Dict['str', ThingFactory]]

    @classmethod
    def register_factory(cls, integration_name: str, thing_type: str, factory: ThingFactory) -> None:
        """
        Register a factory for building of instance of corresponding thing type

        :param integration_name: a name of integration to which this ThingFactory belongs
        :param thing_type: a name of thing type, for which thing factory is registered.
        :param factory: an instance of thing factory that will be used for building
            of those type of things.
        :return: None
        """
        integration_factories = cls.__registry.get(integration_name, dict())
        integration_factories[thing_type] = factory

        cls.__registry[integration_name] = integration_factories

    @classmethod
    def resolve_factory(cls, integration_name: str, thing_type: str, default: ThingFactory or None = None) -> ThingFactory or None:
        """
        Returns an instance of ThingFactory that must be used for building of
        specified type of things.

        :param integration_name: a name of integration to which this ThingFactory belongs
        :param thing_type: a type of thing that ThingFactory is responsible for
        :param default: object to be returned if related ThingFactory is not found
        :return: an instance of ThingFactory or None if it's not found
        """
        integration_factories = cls.__registry.get(integration_name, dict())

        return integration_factories.get(thing_type, default)

    @classmethod
    def remove_factory(cls, integration_name: str, thing_type: str) -> None:
        """
        Removes an instance of thing factory, that is associated with specified thing type

        :param integration_name: a name of integration to which this ThingFactory belongs
        :param thing_type: a type of thing that ThingFactory was responsible for
        :return: None
        """
        integration_factories = cls.__registry.get(integration_name, dict())

        integration_factories.pop(thing_type)
