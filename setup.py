#!/usr/bin/env python
from setuptools import setup

VERSION = "1.0.0"

setup(
    author="Jonas Hagen",
    author_email="jonas.hagen@iap.unibe.ch",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python 3.6",
    ],
    description="Periodically retrieve data from different sources.",
    license="MIT",
    maintainer="Jonas Hagen",
    maintainer_email="jonas.hagen@iap.unibe.ch",
    name="databird",
    packages=["databird", "databird_drivers.standard"],
    python_requires=">=3.5.*, <4",
    version=VERSION,
    url="https://github.com/jonas-hagen/databird",
    download_url="https://github.com/jonas-hagen/databird/archive/databird-{v}.tar.gz".format(
        v=VERSION
    ),
    install_requires=[
        "ruamel.yaml",
        "dict-recursive-update",
        "frozendict",
        "mr.bob",
        "click",
    ],
    entry_points="""
        [console_scripts]
        databird=databird.cli:cli
    """,
)
