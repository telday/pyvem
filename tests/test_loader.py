
import json
import os
import random
import unittest
import pathlib
import pyvem.loader as l
from pyvem.environment import Environment as e


class TestLoader(unittest.TestCase):
    def tearDown(self):
        index = pathlib.Path('.index')
        if index.exists():
            os.remove(index.resolve())

    def generate_index_file_data(self):
        """Generates a list of dict, each dict is a serialized env"""
        #TODO should generate better data here
        args = dict()
        for i in e.OPTIONAL_KWARGS + e.REQUIRED_KWARGS:
            args[i] = random.randint(0, 100)
        return [args]

    def test_load_index(self):
        """Tests the load index function"""
        args = self.generate_index_file_data()
        data = dict()

        for i in range(len(args)):
            data[i] = args[i]
        data = json.dumps(data)

        with open('.index', 'w') as tf:
            tf.write(data)

        loader = l.Loader('.')
        envs = loader.load_index('.index')
        self.assertEqual(len(envs), len(args))

        #This test will fail if order is not preserved
        for environment in range(len(args)):
            for kwarg in args[environment]:
                arg = envs[environment].__getattribute__(kwarg)
                self.assertEqual(arg, args[environment][kwarg])

    def test_serialize(self):
        """Tests the serialize function"""
        data = self.generate_index_file_data()
        environments = [e(**i) for i in data]

        loader = l.Loader('.')
        loader.serialize_environments(environments, '.index')

        with open('.index', 'r') as tf:
            serialized_data = tf.read()
            serialized_data = json.loads(serialized_data)
        
        for environment in range(len(data)):
            for kwarg in data[environment]:
                self.assertEqual(serialized_data[str(environment)][kwarg], data[environment][kwarg])
