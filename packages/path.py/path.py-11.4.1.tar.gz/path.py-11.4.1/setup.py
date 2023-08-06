#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import setuptools

name = 'path.py'
description = 'A module wrapper for os.path'
nspkg_technique = 'native'
"""
Does this package use "native" namespace packages or
pkg_resources "managed" namespace packages?
"""

params = dict(
    name=name,
    use_scm_version=True,
    author="Jason Orendorff",
    author_email="jason.orendorff@gmail.com",
    maintainer="Jason R. Coombs",
    maintainer_email="jaraco@jaraco.com",
    description=description or name,
    url="https://github.com/jaraco/" + name,
    py_modules=['path', 'test_path'],
    python_requires='>=2.7,!=3.1,!=3.2,!=3.3',
    install_requires=[
        'importlib_metadata>=0.5',
        'backports.os; python_version=="2.7" and sys_platform=="linux2"',
    ],
    extras_require={
        'testing': [
            # upstream
            'pytest>=3.5,!=3.7.3',
            'pytest-sugar>=0.9.1',
            'collective.checkdocs',
            'pytest-flake8',

            # local
            'appdirs',
            'packaging',

            # required for checkdocs on README.rst
            'pygments',
        ],
        'docs': [
            # upstream
            'sphinx',
            'jaraco.packaging>=3.2',
            'rst.linker>=1.9',

            # local
        ],
    },
    setup_requires=[
        'setuptools_scm>=1.15.0',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
    },
)
if __name__ == '__main__':
    setuptools.setup(**params)
