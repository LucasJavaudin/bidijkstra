#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'bidijkstra'
DESCRIPTION = 'Different implementations of Bidirectional Dijkstra Algorithm.'
URL = 'https://github.com/LucasJavaudin/bidijkstra'
EMAIL = 'lucas.javaudin@ens-paris-saclay.fr'
AUTHOR = 'Lucas Javaudin & François Phe'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '1.0.0'

# What packages are required for this module to be executed?
REQUIRED = [
    'Cython', 'matplotlib', 'networkx', 'numpy',
]

# What packages are optional?
EXTRAS = {
    'osm': ['osmnx']
}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=['bidijkstra'],
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='GPLv3+',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
