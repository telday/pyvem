"""
Configuration options for both individual environments
and the pyvem environment manager
"""
import pathlib


class Config(object): #pylint: disable=useless-object-inheritance
    """Represents the configuration of a virtual Environment"""

    def __init__(self):
        self.attributes = {
            "system_site_packages": False,
            "clear": False,
            "symlinks": False,
            "upgrade": False,
            "with_pip": False,
            "prompt": None,
        }

    @property
    def values(self):
        """Gets the config values as a dictionary"""
        return self.attributes


class SystemConfig(object): #pylint: disable=useless-object-inheritance
    """Represents the config of the entire manager

    Attributes:
        environment_path (pathlib.Path): The directory where the environment
            data is stored
    """
    DEFAULT_INDEX_FILE_NAME = '.index'

    def __init__(self):
        # TODO use environmental variables to determine the environment path
        self.environment_path = pathlib.Path(r"C:\Users\ewright\Documents\environments")
