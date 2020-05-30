import venv
import pyvem.config

class Environment(venv.EnvBuilder):
    """Represents details about an environment, just acts as a setter/getter

    Attributes:
        prompt
        python_version
        with_pip
        upgrade
        symlinks
        clear
        system_site_packages
    """
    def __init__(
            self,
            prompt,
            python_version=None,
            with_pip=True,
            upgrade=False,
            symlinks=False,
            clear=False,
            system_site_packages=False
        ):
        """Gives every kwarg an attribute"""
        args = locals()
        args.pop('self')
        args.pop('__class__')
        self.python_version = args.pop('python_version')
        self.args = args
        super().__init__(**args)

    def _asdict(self):
        return self.args

    def create(self):
        path_ = pyvem.config.get_pyvem_home() / self.prompt
        super().create(path_)
