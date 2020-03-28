"""

"""
import json
import logging
import pathlib
import pyvem.config as config
import pyvem.environment

class Loader:
    """Helps load and save environment data to the index file

    Attributes:
        pyvem_home_path (pathlike): The pyvem home folder path, this is where
            the index and environment files are stored
    """
    def __init__(self, pyvem_home_path):
        self.pyvem_home_path = pathlib.Path(pyvem_home_path)
        self.logger = logging.getLogger(config.LOGGER_NAME)

    def load_index(self, filename=config.DEFAULT_INDEX_FILE_NAME):
        """Loads the index file into memory
        
        Args:
            filename (str): The name of the index file in the home dir
        Returns:
            list[Environment]: A list of the environments in the index file
        """
        index_file = self.pyvem_home_path / filename
        if not index_file.exists():
            raise FileNotFoundError("Error finding the pyvem index file:",
                    "{}".format(index_file))

        self.logger.info('Opening index file {filename}'.format(filename=index_file.resolve()))
        with open(index_file, 'r') as f:
            data = f.read()
            index_file_data = json.loads(data)

        environments = list()
        for i in index_file_data.values():
            environments.append(pyvem.environment.Environment(**i))
        self.logger.info('Index file loaded, created env list')
        return environments
        

    def serialize_environments(self, environments, filename=config.DEFAULT_INDEX_FILE_NAME):
        """Saves the environment data into the index file
        
        Args:
            filename (str): The name of the index file in the home dir
            environments (list[Environment]): The environments to serialize
        """
        data = dict()
        for i in range(len(environments)):
            data[i] = environments[i].defined_kwargs
        self.logger.info('Serialized environment list to json format')
        data = json.dumps(data)
        with open(self.pyvem_home_path / filename, 'w') as f:
            f.write(data)
        self.logger.info('Wrote serialized data to {filename}'.format(filename=(self.pyvem_home_path / filename).resolve()))
