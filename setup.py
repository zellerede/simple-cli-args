#!/usr/bin/env python3

""" To publish a version:
=============================
  *  increase the version number
  *  py3 setup.py sdist
  *  twine upload dist/*
"""

from setuptools import setup

with open("README.md") as f:
    long_description = f.read()


setup(
    name="simple_cli_args",
    version="1.01",
    packages=['simple_cli_args'],
    author='Bertalan Pecsi',
    author_email='zellerede@gmail.com',
    description='An enhancement of argparse package for its simplest usages',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/zellerede/simple-cli-args',
    keywords='argparse cli cli-args cli_args simple-cli-args simple_cli_args',
    install_requires=["termcolor"],
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
