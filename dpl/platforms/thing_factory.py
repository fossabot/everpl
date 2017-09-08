# Include standard modules
# Include 3rd-party modules
# Include DPL modules
from dpl.things import Thing


class ThingFactory(object):
    """
    ThingFactory is a class that have only one method called 'build'
    that builds an instance of thing by specified configuration.
    """
    @staticmethod
    def build(*args, **kwargs) -> Thing:
        """
        Build: create a specific instance of thing by specified params

        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: an instance of Thing
        """
        raise NotImplementedError
