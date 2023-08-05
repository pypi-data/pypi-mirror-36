import os
import re
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('blackfynn/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'requirements.txt'), mode='r', encoding='utf-8') as f:
    reqs = [line.strip() for line in f if not line.startswith('#')]

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "blackfynn",
    version = version,
    author = "Blackfynn, Inc.",
    author_email = "mark@blackfynn.com",
    description = "Python client for the Blackfynn Platform",
    long_description = long_description,
    packages=find_packages(),
    package_dir={'blackfynn': 'blackfynn'},
    setup_requires=['cython'],
    install_requires = reqs,
    python_requires='<3',
    entry_points = {
        'console_scripts': [
            'bf=blackfynn.cli.bf:blackfynn_cli',
        ]
    },
    license = "",
    keywords = "blackfynn client rest api",
    url = "http://www.blackfynn.com",
    download_url = "",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
