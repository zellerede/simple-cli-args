#!/usr/bin/env python3

from setuptools import setup

with open("README.md") as f:
    long_description = f.read()


setup(
    name="simple_cli_args",
    version="0.20",
    packages=['simple_cli_args'],
    author='Bertalan Pecsi',
    author_email='zellerede@gmail.com',
    description='An enhancement of argparse package for its simplest usages',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/zellerede/simple-cli-args',
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
)
