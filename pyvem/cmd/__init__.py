import argparse

import pyvem.generator
import pyvem.index_manager

def get_environment_name_list():
    index_manager = pyvem.index_manager.IndexManager()
    envs = index_manager.get_environments()
    names = [i.prompt for i in envs]
    for i in names:
        print(i)

def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help='List all environments', action='store_true')
    parser.add_argument('-c', '--create', type=str, help='Create a new environment')

    return parser

def run():
    parser = setup_parser()
    args = parser.parse_args()
    if args.create:
        pyvem.generator.from_prompt(args.create)
    elif args.list:
        pyvem.get_environment_name_list()
