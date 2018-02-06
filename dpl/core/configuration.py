"""
Contains a Configuration class
"""

import os
import logging
import shutil
from typing import Any, MutableMapping

import yaml

import dpl


# Path to the file with default config values
PATH_OF_DEFAULT_CONFIG = os.path.join(
    dpl.DPL_INSTALL_PATH,
    "internal_config",
    "default_config.yaml"
)


logger = logging.getLogger(__name__)


class Configuration(object):
    """
    This class allows to access everpl's configuration.
    Supports loading of configuration from the config file,
    loading of default configuration and on-the-fly
    redefinition of configuration parameters.
    """
    def __init__(self):
        """
        Initializes configuration with default settings
        """
        self._data = {}
        self.load_config(PATH_OF_DEFAULT_CONFIG)

    def load_config(self, config_path: str) -> None:
        """
        Loads configuration from the specified file. All
        existing values will be overridden

        :param config_path: a path to the config file to be
               read
        :return: None
        """
        with open(config_path) as f:
            self._data = yaml.safe_load(f)

    def load_or_create_config(self, config_path: str) -> None:
        """
        Loads configuration from the specified file. Creates
        a new file with default settings if there is not
        existing file by the specified path. All existing
        values will be overridden

        :param config_path: a path to the config file to be
               read
        :return: None
        """
        if not os.path.exists(config_path):
            logging.warning("There is no config file by the specified path. Attempting to create a new one...")
            assert(config_path != PATH_OF_DEFAULT_CONFIG)
            self._copy_default_config(to_path=config_path)

        self.load_config(config_path)

    def _copy_default_config(self, to_path: str) -> None:
        """
        Attempts to copy the default configuration to the specified
        path. Creates parent directories if needed

        :param to_path: a target path for a new config file
        :return: None
        """
        base_path = os.path.dirname(to_path)

        if not os.path.exists(base_path):
            os.makedirs(to_path, mode=0o755)

        shutil.copy(PATH_OF_DEFAULT_CONFIG, to_path)

    def get_by_subsystem(self, subsystem_name: str) -> MutableMapping[str, Any]:
        """
        Allows to get configuration values for the specified
        subsystem

        :param subsystem_name: a name to subsystem for which
               configuration must to be fetched
        :return: config values for the specified subsystem
        """
        return self._data[subsystem_name]
