#!/usr/bin/env python
import setuptools

VERSION = "0.7.0"

with open("README.md", "r") as fh:
    fh.readline()  # do not include ribbons
    long_description = fh.read()

setuptools.setup(
    author="Jonas Hagen",
    author_email="jonas.hagen@iap.unibe.ch",
    classifiers=["Operating System :: OS Independent"],
    description="Keeps a local data repository up to date with different remote data sources.",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
        "rq",
        "redis",
        "flask",
        "rq-dashboard",
    ],
    entry_points="""
        [console_scripts]
        databird=databird.cli:cli
    """,
)
