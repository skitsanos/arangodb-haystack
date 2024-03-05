"""
Setup script for the haystack-arangodb package.

This setup script uses setuptools to configure the packaging of the arangodb-haystack library,
which provides an ArangoDB DocumentStore implementation for the Haystack framework.
It includes metadata about the package such as its name, version, author information,
description, and more. The script also specifies package dependencies which are required
for the library to function correctly.

The arangodb-haystack library facilitates integration between the Haystack NLP framework
and ArangoDB, enabling efficient storage, retrieval, and querying of documents
in a scalable manner for NLP applications.

Dependencies include python-arango for ArangoDB database interactions and haystack-ai
for compatibility with the Haystack framework.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="arangodb-haystack",
    version="0.1.0",
    author="Skitsanos",
    author_email="info@skitsanos.com",
    description="A Haystack DocumentStore implementation for ArangoDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skitsanos/arangodb-haystack",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "python-arango>=7.9.0",
        "haystack-ai>=2.0.0",
    ],
    python_requires='>=3.6',
)
