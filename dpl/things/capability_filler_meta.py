"""
This class contains a definition of the CapabilityFiller metaclass.
"""
import inspect
from typing import Iterable, Generator


class CapabilityFiller(type):
    """
    CapabilityFiller is a metaclass which intercepts the class
    creation process, discovers all Capabilities (parent classes)
    of the class and fills the corresponding ``_capabilities``
    private property of the class with the names of all Capabilities
    which was implemented by the class
    """

    def __new__(mcs, name, bases, class_dict):
        cls = type.__new__(mcs, name, bases, class_dict)

        mros = inspect.getmro(cls)

        cls._capabilities = tuple(
            mcs._capability_list_generator(source=mros)
        )

        return cls

    @staticmethod
    def _capability_list_generator(source: Iterable) -> Generator[str, None, None]:
        """
        A generator which extracts capability names from the
        specified list of Capabilities

        :param source: a list of parent classes to be parsed
        :return: a generator of Capability names
        """
        attr = '_capability_name'

        for i in source:
            if attr not in i.__dict__:
                continue

            name = getattr(i, attr, None)

            assert name is not None

            yield name
