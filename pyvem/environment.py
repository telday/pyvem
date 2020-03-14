
VALID_KWARGS = ['system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip','installed_packages', 'python_version']
REQUIRED_KWARGS = ['prompt',  'location']

class Environment:
    """Represents details about an environment, just acts as a setter/getter"""
    def __init__(self, **kwargs):
        """Gives every kwarg an attribute"""
        for i in REQUIRED_KWARGS:
            if i not in kwargs.keys():
                raise AttributeError("Environment requires args",
                        "{}".format(REQUIRED_KWARGS))

        for i in kwargs:
            if i not in VALID_KWARGS + REQUIRED_KWARGS:
                raise AttributeError(
                            "{} is not a valid attribute for Environment"
                        )
            self.__setattr__(i, kwargs[i])
