"""Provides functionality for generating the files for a new venv"""
import venv
import pathlib

import pyvem.environment

def generate_batch_file(environment: pyvem.environment.Environment):
    """Generates the batch files which correspond to each environment

    Args:
        directory (Path): The directory to put the batch file in
        env (Path): The path to the environment directory
        config: The config of the env to make a batch file for
    """
    pass

def generate_environment(environment: pyvem.environment.Environment):
    """
    Generates the new venv in the given directory with the given config values

    Args:
        directory (Path): The directory to use
        config (tmp): The config information
    Returns:
        dict: The representation of the created environment
    Raises:
        Exception: On failure to create environment
    """
    '''
    builder = venv.EnvBuilder(**config.values)
    builder.create(directory.resolve())

    index = dict()
    if builder.prompt:
        name = builder.prompt
    else:
        name = directory.name

    index[name] = {**config.values}
    index[name]["path"] = directory.resolve()
    return index
    '''
