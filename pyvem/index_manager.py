import os
import pathlib
import json

import pyvem.environment

class IndexManager:

    def load_index_file(self):
        filename = self.get_index_file_location()
        try:
            with open(filename, 'r') as index_file:
                data = index_file.read()
            json_data = json.loads(data)
        except FileNotFoundError:
            json_data = json.loads('{}')
        return json_data

    def get_environments(self):
        data = self.load_index_file()
        environments = list()
        for i in data:
            env = pyvem.environment.Environment(**data[i])
            environments.append(env)
        return environments

    def add_environment(self, environment):
        current_environments = self.get_environments()
        current_environments.append(environment)
        self.save_environments(current_environments)
        
    def save_environments(self, environments):
        data = dict()
        for i in range(len(environments)):
            data[i] = environments[i]._asdict()
        json_data = json.dumps(data)
        filename = self.get_index_file_location()
        with open(filename, 'w') as index_file:
            index_file.write(json_data)

    def get_index_file_location(self):
        file_location = pathlib.Path(os.environ['HOME'])
        return (file_location / 'pyvem' ) / '.index'
