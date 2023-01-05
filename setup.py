import setuptools
import platform
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="clinproc",
    version="0.1.42",
    author="James Kelly",
    author_email="mrkellyjam@gmail.com",
    description="library for processing clinical trials data from clinicaltrials.gov",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/semajyllek/clinproc", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['lxml', 'spacy == 3.0.1', 'scispacy', 'negspacy', 'scipy'],
)