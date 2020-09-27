import argparse
import sys
import shutil

import pyvem.config
import pyvem.generator
import pyvem.index_manager
from pyvem.exceptions import EnvironmentException

def run():
    parser = setup_parser()
    args = parser.parse_args(args=sys.argv[1:])
    if args.create:
        pyvem.generator.from_prompt(args.create)
    elif args.delete:
        delete_environment(args.delete)
    elif args.list:
        get_environment_name_list()

def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help='List all environments', action='store_true')
    parser.add_argument('-c', '--create', help='Create a new environment')
    parser.add_argument('-d', '--delete', help='Delete an environment')

    return parser

def get_environment_name_list():
    index_manager = pyvem.index_manager.IndexManager()
    envs = index_manager.get_environments()
    names = [i.prompt for i in envs]
    for i in names:
        print(i)

def delete_environment(prompt):
    # TODO should you be able to delete the activated env?
    pyvem_home = pyvem.config.get_pyvem_home()

    env_dir = pyvem_home / prompt
    if not env_dir.exists():
        raise EnvironmentException(f"Unable to find environment: {prompt}")
    shutil.rmtree(env_dir)
    
    index_manager = pyvem.index_manager.IndexManager()
    index_manager.delete_environment(prompt)
