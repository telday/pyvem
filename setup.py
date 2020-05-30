
import setuptools

setuptools.setup(
            name = "an_example_pypi_project",
            version = "0.0.4",
            author = "Ellis Wright",
            author_email = "ejw393@gmail.com",
            description = "A python virtual environment manager",
            license = "MIT",
            packages=['pyvem'],
            entry_points = {
                'console_scripts': [
                    'pyvem = pyvem.cmd:run',
                ]
            }
        )
