from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="abtestingstrategiesbackend",
    version="0.1.1",
    description="ab testing research",
    license=license,
    long_description=long_description,
    author="Victor Dremov",
    author_email="victor.dremov@gmail.com",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
)

