"""Provides functionality for generating the files for a new venv"""
import venv
import pathlib
import sys

import pyvem.environment
import pyvem.index_manager
import pyvem.config

from . import __path__

def generate_pyvem_home():
    home = pathlib.Path(pyvem.config.DEFAULT_PYVEM_HOME)
    if not home.exists():
        home.mkdir()

def generate_batch_file(default_path = pyvem.config.DEFAULT_PYVEM_HOME):
    """Generates the batch files which correspond to each environment

    Args:
        directory (Path): The directory to put the batch file in
        env (Path): The path to the environment directory
        config: The config of the env to make a batch file for
    """
    default_path = pathlib.Path(default_path)
    template = pathlib.Path(__path__[0]) / 'bin\\pyvem.bat.template'
    with open(template, 'r') as template_file:
        data = template_file.read()
    data = data.format(default_pyvem_path=default_path)
    generate_pyvem_home()
    home = pathlib.Path(pyvem.config.DEFAULT_PYVEM_HOME)
    with open(default_path / 'pyvem.bat', 'w') as f:
        f.write(data)

def generate_environment(path_, environment: pyvem.environment.Environment):
    """
    Generates the new venv in the given directory with the given config values

    Args:
        path_ (pathlike): The directory to put the environment in
        environment(Environment): The environment to create
    Raises:
        Exception: On failure to create environment
    """
    builder = venv.EnvBuilder(**environment.optional_kwargs())
    builder.create(path_)

    im = pyvem.index_manager.IndexManager()
    im.add_environment(environment)



def create_new_environment():
    if len(sys.argv) < 2:
        print("Need to specify the environment to create")
        exit(1)
    name = sys.argv[1]
    e = pyvem.environment.Environment(prompt=name, location=f'.\\{name}', python_version=str(sys.version))
    self.generate_environment(e)
