#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

setup(
    name="neuropycon_data",
    version='0.0.dev3',
    packages=find_packages(),
    author="David Meunier",
    description="Data for neuropycon testing",
    include_package_data=True,
    install_requires=[]
)
