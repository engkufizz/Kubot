"""Setup for Kubot 100% pure-Python agentic harness."""

import os
from setuptools import setup, find_packages

_ROOT = os.path.dirname(os.path.abspath(__file__))


def _root_py_modules():
    try:
        names = os.listdir(_ROOT)
    except OSError:
        return []
    return sorted(
        name[:-3]
        for name in names
        if name.endswith(".py") and name != "setup.py"
    )


setup(
    packages=find_packages(),
    py_modules=_root_py_modules(),
)

