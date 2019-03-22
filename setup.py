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
    license="mit",
    maintainer="Jonas Hagen",
    maintainer_email="jonas.hagen@iap.unibe.ch",
    name="databird",
    packages=["databird"],
    python_requires=">=3.5.*, <4",
    version=VERSION,
    install_requires=["pymlconf"],
)
