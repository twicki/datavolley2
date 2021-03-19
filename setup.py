#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

requirements = []

setup_requirements = []

test_requirements = []

setup(
    author="Tobias Wicky",
    author_email="tobias@volleyrueschlikon.ch",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: MIT",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="scouting",
    install_requires=requirements,
    extras_require={},
    license="MIT license",
    include_package_data=True,
    keywords="scouting",
    name="tvrscouting",
    packages=find_packages(include=["tvrscouting", "tvrscouting.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    version="0.1.0",
    zip_safe=False,
)
