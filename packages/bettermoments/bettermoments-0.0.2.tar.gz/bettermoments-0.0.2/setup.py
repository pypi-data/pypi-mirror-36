#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bettermoments",
    version="0.0.2",
    author="Richard Teague & Daniel Foreman-Mackey",
    py_modules=["bettermoments"],
    url="https://github.com/richteague/bettermoments",
    license="MIT",
    description=("A robust method for inferring line-of-sight velocities from "
                 "Doppler shifted spectra"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["numpy"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    zip_safe=True,
)
