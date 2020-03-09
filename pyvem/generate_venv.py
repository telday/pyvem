"""Provides functionality for generating the files for a new venv"""
import venv
import pathlib


def create_new_venv(directory: pathlib.Path, config):
    """
    Generates the new venv in the given directory with the given config valuies

    Args:
        directory (str): The directory to use
        config (tmp): The config information
    Returns:
        dict: The representation of the created environment
    Raises:
        Exception: On failure to create environment
    """
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
