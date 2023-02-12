#!/usr/bin/env python

import os
import sys

import setuptools

PACKAGE_NAME = "toothbrush"
MINIMUM_PYTHON_VERSION = "3.7"


def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version < MINIMUM_PYTHON_VERSION:
        sys.exit(f"Python {MINIMUM_PYTHON_VERSION}+ is required.")


def read_package_variable(key, filename="__init__.py"):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join(PACKAGE_NAME, filename)
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(" ", 2)
            if parts[:-1] == [key, "="]:
                return parts[-1].strip("'")
    sys.exit(f"'{key}' not found in '{module_path}'")


def build_description():
    """Build a description for the project from documentation files."""
    readme = open("README.md").read()
    changelog = open("CHANGELOG.md").read()
    return readme + "\n" + changelog


check_python_version()

setuptools.setup(
    name=read_package_variable("__project__"),
    version=read_package_variable("__version__"),

    description="Sample project generated from jacebrowning/template-python.",
    url="https://github.com/thomasvincent/toothbrush",
    author="Thomas Vincent",
    author_email="thomasvincent@gmail.com",

    packages=setuptools.find_packages(),

    entry_points={"console_scripts": [
        "toothbrush-cli = toothbrush.cli:main",
        "toothbrush-gui = toothbrush.gui:main",
    ]},

    long_description=build_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        # TODO: update this list to match your application: https://pypi.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 1 - Planning",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],

    install_requires=[
        # TODO: Add your library's requirements here
        "click ~= 6.0",
        "minilog ~=0.2.1",
    ]
)
