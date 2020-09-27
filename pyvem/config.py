"""
Configuration options for both individual environments
and the pyvem environment manager
"""
import os
import pathlib
import logging

import yaml

DEFAULT_INDEX_FILE_NAME = '.index'
LOGGER_NAME = "pyvem_logger"

DEFAULT_PYVEM_HOME = pathlib.Path.home() / '.pyvem'

def get_pyvem_home():
    return DEFAULT_PYVEM_HOME

def get_pyvem_config():
    conf = dict()
    config_file = self.get_pyvem_home() / 'config.yaml'
    with open(config_file.resolve(), 'r') as cf:
        conf = yaml.load(cf.read())
    return conf
