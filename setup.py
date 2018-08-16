#!/usr/bin/env python
"""
traffic_info from https://github.com/Da-Juan/traffic_info.

setup.py from https://github.com/kennethreitz/setup.py
"""
import io
import os

from setuptools import setup

CMDCLASS = {}
try:
    from sphinx.setup_command import BuildDoc

    CMDCLASS["build_sphinx"] = BuildDoc
except ImportError:
    print("WARNING: sphinx not available, not building docs")

# Package meta-data.
NAME = "traffic_info"
DESCRIPTION = "Send traffic info screenshots by email."
URL = "https://github.com/Da-Juan/traffic_info"
EMAIL = "rouanet.n@gmail.com"
AUTHOR = "Nicolas Rouanet"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = None

REQUIRED = ["configargparse", "jinja2", "selenium"]

TESTS_REQUIRED = [
    "bandit",
    "black",
    "flake8",
    "flake8-bugbear",
    "flake8-colors",
    "flake8-docstrings",
    "flake8-import-order",
    "pep8-naming",
    "pylint",
]

DEV_REQUIRED = [
    "bpython",
    "m2r",
    "pre-commit",
    "Sphinx",
    "sphinx-rtd-theme",
    "sphinxcontrib-napoleon",
] + TESTS_REQUIRED

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = "\n" + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
ABOUT = {}
if not VERSION:
    with open(os.path.join(HERE, NAME, "__version__.py")) as f:
        exec(f.read(), ABOUT)  # pylint: disable=W0122
else:
    ABOUT["__version__"] = VERSION

setup(
    name=NAME,
    version=ABOUT["__version__"],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=["traffic_info"],
    install_requires=REQUIRED,
    include_package_data=True,
    scripts=["bin/traffic-info", "bin/install_chromedriver.sh"],
    extras_require={"tests": TESTS_REQUIRED, "dev": DEV_REQUIRED},
    cmdclass=CMDCLASS,
    command_options={
        "build_sphinx": {
            "project": ("setup.py", NAME),
            "version": ("setup.py", ABOUT["__version__"]),
            "release": ("setup.py", ABOUT["__version__"] + ".0"),
            "source_dir": ("setup.py", "docs"),
        }
    },
    license="BSD",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
)
