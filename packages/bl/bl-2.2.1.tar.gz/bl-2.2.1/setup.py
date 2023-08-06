
config = {
  "name": "bl",
  "version": "2.2.1",
  "description": "Black Earth core library",
  "url": "https://github.com/BlackEarth/bl",
  "author": "Sean Harrison",
  "author_email": "sah@blackearthgroup.com",
  "license": "LGPL 3.0",
  "classifiers": [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3"
  ],
  "entry_points": {},
  "install_requires": [],
  "extras_require": {
    "dev": ['twine'],
    "test": []
  },
  "package_data": {
    "bl": []
  },
  "data_files": [],
  "scripts": []
}

import os, json
from setuptools import setup, find_packages
from codecs import open

path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(path, 'README.rst'), encoding='utf-8') as f:
    read_me = f.read()

setup(
    long_description=read_me,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    **config
)
