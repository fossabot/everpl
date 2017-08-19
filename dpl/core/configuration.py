# Include standard modules
import json
import os
from typing import List, Dict

# Include 3rd-party modules
# Include DPL modules


def check_dir_path(dir_path: str) -> None:
    if not isinstance(dir_path, str):
        raise ValueError("config dir must be a string - path to folder with config files")

    if not os.path.exists(dir_path):
        raise ValueError("specified path does not exist")

    if not os.path.isdir(dir_path):
        raise ValueError("specified path is not a directory")


def get_dir_structure(dir_path: str) -> dict:
    dir_structure = dict()

    for root_path, dirs, files in os.walk(dir_path, topdown=False):
        root_name = os.path.basename(root_path)
        dir_structure[root_name] = list()

        for name in files:
            if name.endswith(".json"):
                dir_structure[root_name].append(os.path.join(root_path, name))

    return dir_structure


class Configuration(object):
    """
    Configuration is a class that is responsible for management and storage
    of all platform configurations and settings.
    """

    # TODO: Rewrite with async approach
    def __init__(self, path: str):
        """
        Constructor which saves a path to configuration directory
        :param path: a path to configuration directory
        """
        check_dir_path(path)

        self._path = path

        self._conf_data = dict()

    def load_config(self) -> None:
        """
        Loads configuration from disk to memory
        :return: None
        """
        # TODO: REWRITE
        conf_structure = get_dir_structure(self._path)

        for subsystem_name in conf_structure:
            self._conf_data[subsystem_name] = list()
            subsystem_elements = self._conf_data[subsystem_name]

            for file_path in conf_structure[subsystem_name]:
                with open(file_path) as file:
                    content = json.load(file)

                    if type(content) != type(subsystem_elements):
                        assert isinstance(content, dict)
                        self._conf_data[subsystem_name] = content
                        continue

                    subsystem_elements.extend(content)

    def save_config(self) -> None:
        """
        Saves configuration on disk
        :return: None
        """
        raise NotImplementedError

    def get_by_subsystem(self, subsystem_name: str) -> Dict or List[Dict]:
        """
        Returns a dict or list of config values that is related to specific subsystem
        :param subsystem_name: subsystem name for request
        :return: configuration values that are related to specified subsystem
        """
        return self._conf_data[subsystem_name]
