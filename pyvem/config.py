"""
Configuration options for both individual environments
and the pyvem environment manager
"""
import os
import pathlib
import logging

DEFAULT_INDEX_FILE_NAME = '.index'
LOGGER_NAME = "pyvem_logger"

DEFAULT_PYVEM_HOME = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + '\\.pyvem'
