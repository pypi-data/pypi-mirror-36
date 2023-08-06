import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="b9y",
    version="0.0.3",
    author="Uli Hitzel",
    author_email="uli.hitzel@gmail.com",
    description="Commandline Interface for Bambleweeny",
    #long_description="Bambleweeny (b9y) is a lightweight HTTP/REST based key-value store and message broker that offers identity, access & quota management. It's fast, easy to use, and well-documented. This module provides a commandline tool to access b9y.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/u1i/bambleweeny",
    packages=['b9y'],
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
