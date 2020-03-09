import json
import pathlib
import pyvem.config
import pyvem.generate_venv
import os

class EnvironmentManager(object):
    """
    Object to be used to get information about the environments
    this program manages
    """
    def __init__(self):
        self.config = pyvem.config.get_system_config()
        
    def add_environment(self, venv_name: str):
        """Generates a new global environment

        Args:
            venv_name (str): The name of the env to add
        """
        path = self.config.environment_path / venv_name
        index_file = self.config.environment_path / self.config.index_file_name
        #TODO what happens if an env with that name already exists?
        info = pyvem.generate_venv.create_new_venv(path, pyvem.config.Config())
        if index_file.exists():
            # If the .index file is a dir for some reasion
            if index_file.is_dir():
                raise FileNotFoundError(\
                            f"Unable to load .index file from {index_file}"
                        )
            # Get all the previous information
            with open(index_file, 'r') as f:
                data = f.read()
            
            # If the string is empty json will raise error so check first
            if not data:
                file_info = dict()
            else:
                file_info = json.loads(data)
        else:
            file_info = dict()
        
        #NOTE this will overwrite any keys in file_info with data from the
        # same keys in info may cause edge case issues
        file_info = {**file_info, **info}

        # This makes sure that a WindowsPath or Path object doesnt accidentally
        # Try to get serialized
        for env in file_info:
            for value in file_info[env]:
                if issubclass(type(file_info[env][value]), pathlib.Path):
                    file_info[env][value] = str(file_info[env][value])

        data = json.dumps(file_info)

        with open(index_file, 'w') as f:
            f.write(data)

    def list_environments(self):
        path = self.config.environment_path
        index_file = path / self.config.index_file_name
