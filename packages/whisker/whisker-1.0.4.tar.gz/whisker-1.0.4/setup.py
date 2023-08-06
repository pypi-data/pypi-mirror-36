#!/usr/bin/env python
# setup.py

"""
Whisker setup file

To use:

    python setup.py sdist

    twine upload dist/*

To install in development mode:

    pip install -e .

"""
# https://packaging.python.org/en/latest/distributing/#working-in-development-mode  # noqa
# http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/
# http://jtushman.github.io/blog/2013/06/17/sharing-code-across-applications-with-python/  # noqa

from setuptools import setup
from codecs import open
from os import path

from whisker.version import VERSION

here = path.abspath(path.dirname(__file__))

# -----------------------------------------------------------------------------
# Get the long description
# -----------------------------------------------------------------------------
long_description = r"""
    Whisker Python client library.
    
    See https://whiskerpythonclient.readthedocs.io/
"""

# *** readthedocs

# -----------------------------------------------------------------------------
# setup args
# -----------------------------------------------------------------------------
setup(
    name='whisker',

    version=VERSION,

    description='Whisker Python client library',
    long_description=long_description,

    # The project's main homepage.
    url='http://www.whiskercontrol.com/',

    # Author details
    author='Rudolf Cardinal',
    author_email='rudolf@pobox.com',

    # Choose your license
    license='Apache License 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        'Natural Language :: English',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',

        'Topic :: System :: Hardware',
        'Topic :: System :: Networking',
    ],

    keywords='whisker research control',

    packages=['whisker'],

    install_requires=[
        'arrow',  # better datetime
        'attrdict',  # dictionaries with attribute-style access
        'cardinal_pythonlib>=1.0.1',
        'colorama',  # colour at the command line
        'colorlog',  # colourful logs
        'dataset',  # databases for lazy people (used by demo)
        'PyQt5',  # Qt for Python
        'Twisted',  # TCP/IP communications
        'typing==3.5.2.2',  # part of stdlib in Python 3.5, but not 3.4
        'pyyaml',  # Yet Another Markup Language
        'sqlalchemy',  # Databases

        # ---------------------------------------------------------------------
        # For development only:
        # ---------------------------------------------------------------------
        # sphinx  # for documentation
        # twine  # for uploading to PyPI
    ],

    entry_points={
        'console_scripts': [
            # Format is 'script=module:function".
            'whisker_test_rawsockets=whisker.test_rawsockets:main',
            'whisker_test_twisted=whisker.test_twisted:main',
        ],
    },
)
