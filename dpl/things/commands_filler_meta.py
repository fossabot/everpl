"""
This class contains a definition of the CommandsFiller metaclass.
"""
import inspect
from typing import Iterable, Generator

from .capability_filler_meta import CapabilityFiller


class CommandsFiller(CapabilityFiller):
    """
    CommandsFiller is a metaclass which intercepts the class creation process,
    discovers all actuator commands from inherited Capabilities
    of the class and fills the corresponding ``_all_commands``
    private property of the class with the names of all commands
    which are provided by the class
    """

    def __new__(mcs, name, bases, class_dict):
        cls = super().__new__(mcs, name, bases, class_dict)

        mros = inspect.getmro(cls)

        cls._all_commands = tuple(
            mcs._commands_list_generator(source=mros)
        )

        return cls

    @staticmethod
    def _commands_list_generator(
            source: Iterable
    ) -> Generator[str, None, None]:
        """
        A generator which extracts command names from the
        specified list of Capabilities

        :param source: a list of parent classes to be parsed
        :return: a generator of command names
        """
        attr = '_commands'

        for i in source:
            if attr not in i.__dict__:
                continue

            commands = getattr(i, attr, None)

            assert isinstance(commands, Iterable)

            for j in commands:
                yield j
