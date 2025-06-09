"""
Setup script for shared schemas package
"""
from setuptools import setup, find_packages

setup(
    name="implodesc-shared",
    version="0.1.0",
    description="Shared schemas and types for Implodesc",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "pydantic>=2.5.0",
    ],
)