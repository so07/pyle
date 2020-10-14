from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="pyle",
    version="0.1.1",
    author="so07",
    author_email="so07git@gmail.it",
    description="Command line parser options of argparse module for date and time filtering positional list of files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/so07/pyle.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
    ],
)
