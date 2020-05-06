#!/usr/bin/env python
from distutils.core import setup
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="DBN",
    version="0.1.0",
    packages=find_packages(),
    # metadata to display on PyPI
    author="Vhenrixon",
    author_email="vhenrixon@gmail.com",
    description="Decentralized Bluetooth Network",
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'note = DBN.main:main'
        ]
    },
    install_requires=[
        'pybluez',
        'python_jwt',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Development Status :: 3 - Alpha"
    ]
)