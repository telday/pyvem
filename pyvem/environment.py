import venv
import logging
import os
import shutil
import subprocess
import sys
import sysconfig
import types

import pyvem.config

logger = logging.Logger(__name__)
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
        self.__dict = dict(args)
        self.__dict['python_version'] = python_version
        super().__init__(**args)

    def _asdict(self):
        return self.__dict

    def create(self):
        path_ = pyvem.config.get_pyvem_home() / self.prompt
        env_dir = os.path.abspath(path_)
        context = self.ensure_directories(env_dir)
        self.create_configuration(context)
        self.setup_python(context)
        self.setup_scripts(context)
        self.post_setup(context)
