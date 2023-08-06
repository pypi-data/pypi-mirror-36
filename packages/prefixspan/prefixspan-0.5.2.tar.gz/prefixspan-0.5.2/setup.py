#! /usr/bin/env python3

from setuptools import setup

url = "https://github.com/chuanconggao/PrefixSpan-py"
version = "0.5.2"

setup(
    name="prefixspan",

    packages=["prefixspan"],
    scripts=["prefixspan-cli"],
    include_package_data=True,

    url=url,

    version=version,
    download_url="{}/tarball/{}".format(url, version),

    license="MIT",

    author="Chuancong Gao",
    author_email="chuancong@gmail.com",

    description="PrefixSpan, BIDE, and FEAT in Python 3",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",

    keywords=[
        "data-mining",
        "pattern-mining"
    ],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],

    python_requires=">= 3",
    install_requires=[
        line.strip() for line in open("requirements.txt")
    ]
)
