#!/usr/bin/env python

from setuptools import setup

setup(
    name="spacegame",
    version="0.1",
    description="",
    author="ecdavis",
    author_email="me@ezdwt.com",
    url="http://github.com/ecdavis/spacegame",
    download_url="https://github.com/ecdavis/spacegame/tarball/master",
    packages=["spacegame", "spacegame.core", "spacegame.modules", "spacegame.universe"],
    test_suite="tests.get_all_tests",
    install_requires=["pants >= 1.0", "pantsmud >= 0.2"],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English"
    ]
)
