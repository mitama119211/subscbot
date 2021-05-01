"""Setup library."""

import pip
import sys

from distutils.version import LooseVersion
from setuptools import find_packages
from setuptools import setup

from subscbot import __version__

if LooseVersion(sys.version) < LooseVersion("3.6"):
    raise RuntimeError(
        f"subscbot requires Python>=3.6 but current version is {sys.version}."
    )
if LooseVersion(pip.__version__) < LooseVersion("19"):
    raise RuntimeError(
        f"pip>=19.0.0 is required but current version is {pip.__version__}."
    )

install_requires = open("requirements.txt").read().splitlines()
setup_requires = ["pytest-runner"]
tests_requires = ["pytest", "hacking", "flake8-docstrings"]

setup(
    name="subscbot",
    version=__version__,
    url="",
    author="",
    description="A package to tweet the number of youtube subscribers.",
    package=find_packages(include=["subscbot"]),
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_requires=tests_requires,
)
