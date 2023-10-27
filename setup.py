from os import path
from setuptools import find_packages  # setup
from cx_Freeze import setup as cx_setup, Executable
import sys

base = None

if sys.platform == "win32":
    base = None

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'VERSION'), encoding='utf-8') as version_file:
    version = version_file.read()

with open(path.join(here, 'requirements.txt')) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [line for line in requirements_file.read().splitlines()
                    if not line.startswith('#')]

executables = [Executable(script=r"bot_gn\bot.py", base=base)]

packages = ["idna"]
options = {
    "build_exe": {
        "packages": packages,
    },
}

cx_setup(
    name="bot_gn",
    version=version,
    description="Python package for a BotCity bot.",
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['docs', 'tests']),
    options=options,
    executables=executables,
    include_package_data=True,
    package_data={
        "bot_gn": [
            # When adding files here, remember to update MANIFEST.in as well,
            # or else they will not be included in the distribution on PyPI!
            # 'path/to/data_file',
            'resources',
        ]
    },
    # install_requires=requirements,
)


# setup(
#     name="bot_gn",
#     version=version,
#     description="Python package for a BotCity bot.",
#     long_description=readme,
#     long_description_content_type='text/markdown',
#     packages=find_packages(exclude=['docs', 'tests']),
#     include_package_data=True,
#     package_data={
#         "bot_gn": [
#             # When adding files here, remember to update MANIFEST.in as well,
#             # or else they will not be included in the distribution on PyPI!
#             # 'path/to/data_file',
#             'resources',
#         ]
#     },
#     install_requires=requirements,
# )
