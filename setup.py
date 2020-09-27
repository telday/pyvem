import os
import pathlib
import setuptools

pyvem_home = pathlib.Path(os.environ['USERPROFILE']) / '.pyvem'

setuptools.setup(
            name = "py-vem",
            version = "0.1.0",
            author = "Ellis Wright",
            author_email = "ejw393@gmail.com",
            description = "A python virtual environment manager",
            license = "MIT",
            packages=setuptools.find_packages('.'),
            install_requires=['pyyaml'],
            include_package_data=True,
            data_files=[(str(pyvem_home.resolve()), ['pyvem/bin/pyvem.bat'])]
        )
