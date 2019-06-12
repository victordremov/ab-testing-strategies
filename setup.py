from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("LICENSE") as f:
    license = f.read()

name = "abtestingstrategiesbackend"
setup(
    name=name,
    version="0.1",
    description="ab testing research",
    license=license,
    long_description=long_description,
    author="Victor Dremov",
    author_email="victor.dremov@gmail.com",
    packages=[name],
)
