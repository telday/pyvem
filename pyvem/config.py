import pathlib

class Config(object):
    """Represents the configuration of a virtual Environment"""
    def __init__(self):
        self.c = {
            'system_site_packages':False,
            'clear': False,
            'symlinks':False,
            'upgrade':False,
            'with_pip':False,
            'prompt':None,
        }

    @property
    def values(self):
        return self.c

class SystemConfig(object):
    """Represents the config of the entire manager

    Attributes:
        environment_path (pathlib.Path): The directory where the environment
            data is stored
    """
    def __init__(self):
        self.environment_path = \
                pathlib.Path(r"C:\Users\ewright\Documents\environments")


def get_system_config():
    return SystemConfig()
