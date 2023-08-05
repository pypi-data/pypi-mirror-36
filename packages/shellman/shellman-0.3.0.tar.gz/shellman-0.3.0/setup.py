#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Setup script.

Uses setuptools.
Long description is README.md.
"""

from __future__ import absolute_import, print_function

import io
import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*names, **kwargs):
    """Read a file in current directory."""
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='shellman',
    version='0.3.0',
    license='ISC',
    description='Write doc in your shell scripts.',
    long_description=re.compile(
        '^<!-- start-badges.*^.. end-badges -->', re.M | re.S
    ).sub('', read('README.md')),
    author=u'Timothee Mazzucotelli',
    author_email='timothee.mazzucotelli@gmail.com',
    url='https://gitlab.com/pawamoy/shellman',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords=[
        'shellman',
    ],
    install_requires=[
        'jinja2'
    ],
    extras_require={
        ':python_version == "2.7"': ['backports.shutil_get_terminal_size']
    },
    entry_points={
        'console_scripts': [
            'shellman = shellman.cli:main',
        ]
    },
)
