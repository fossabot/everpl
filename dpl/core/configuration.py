class Configuration(object):
    """
    Configuration is a class that is responsible for management and storage
    of all platform configurations and settings.
    """
    def __init__(self, path: str):
        """
        Constructor which saves a path to configuration directory
        :param path: a path to configuration directory
        """
        self._path = path

    def load_config(self) -> None:
        """
        Loads configuration from disk to memory
        :return: None
        """
        raise NotImplementedError

    def save_config(self) -> None:
        """
        Saves configuration on disk
        :return: None
        """
        raise NotImplementedError

    def get_by_subsystem(self, subsystem_name: str) -> dict:
        """
        Returns a dict of config values that is related to specific subsystem
        :param subsystem_name: subsystem name for request
        :return: configuration values that are related to specified subsystem
        """
        raise NotImplementedError
