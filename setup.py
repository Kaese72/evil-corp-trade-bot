#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="Distutils",
    version="1.0",
    description="Python evil bot",
    author="Kaese",
    packages=find_packages(".", include=["evilbot*"]),
)
