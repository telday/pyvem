

class Environment:
    """Represents details about an environment, just acts as a setter/getter

    Attributes:
        OPTIONAL_KWARGS: A list of optional kwargs for the constructor
        REQUIRED_KWARGS: A list of required kwargs for the constructor
    """

    OPTIONAL_KWARGS = ['system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip','installed_packages', 'python_version']
    REQUIRED_KWARGS = ['prompt',  'location']

    def __init__(self, **kwargs):
        """Gives every kwarg an attribute"""
        self._defined_kwargs = kwargs

        for i in self.REQUIRED_KWARGS:
            if i not in kwargs.keys():
                raise AttributeError("Environment requires args",
                        "{}".format(self.REQUIRED_KWARGS))

        for i in kwargs:
            if i not in self.OPTIONAL_KWARGS + self.REQUIRED_KWARGS:
                raise AttributeError(
                            "{} is not a valid attribute for Environment"
                        )
            self.__setattr__(i, kwargs[i])

    @property
    def defined_kwargs(self):
        return self._defined_kwargs
