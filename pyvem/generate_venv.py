import venv

def create_new_venv(directory: str, config):
    """
    Generates the new venv in the given directory with the given config valuies

    Args:
        directory (str): The directory to use
        config (tmp): The config information
    Raises:
        Exception: On failure to create environment
    """
    builder = venv.EnvBuilder(**config.values)
    builder.create(directory)
