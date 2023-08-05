#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-stubprocess',
    version='0.1.0',
    author='Alex Thompson',
    author_email='aptbosox@gmail.com',
    maintainer='Alex Thompson',
    maintainer_email='aptbosox@gmail.com',
    license='MIT',
    url='https://github.com/aptbosox/pytest-stubprocess',
    description='Provide stub implementations for subprocesses in Python tests',
    long_description=read('README.rst'),
    py_modules=['pytest_stubprocess'],
    python_requires='>=3.6',
    install_requires=[
        'attrs',
        'pytest>=3.5.0',
        'pytest-mock',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'stubprocess = pytest_stubprocess',
        ],
    },
)
