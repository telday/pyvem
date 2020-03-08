

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
