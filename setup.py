

# I honestly don't know what this code does and copied it from an excellent blog post: https://towardsdatascience.com/deep-dive-create-and-publish-your-first-python-library-f7f618719e14

from setuptools import setup,find_packages

from codecs import open
from os import path



HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="clinproc",
    version="0.1.0",
    description="library for processing clinical trials data from clinicaltrials.gov",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="James Kelly",
    author_email="mrkellyjam@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    install_requires=[
        "lxml", 
        "scispacy", 
        "negspacy"
        ]
)

