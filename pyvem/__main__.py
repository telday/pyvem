import pyvem.environment
import pyvem.generator
import sys

def create_new_environment():
    if len(sys.argv) < 2:
        print("Need to specify the environment to create")
        exit(1)
    name = sys.argv[1]
    e = pyvem.environment.Environment(prompt=name, location=f'.\\{name}', python_version=str(sys.version))
    pyvem.generator.generate_environment(e)

create_new_environment()
