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