from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='clinproc',  
    version='0.1.20',
    description='library for processing clinical trials data from clinicaltrials.gov',
    long_description=long_description,
    long_description_content_type='text/markdown',  
    url='https://github.com/semajyllek/clinproc',
    author='James Kelly',
    author_email='mrkellyjam@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='clinical, trials',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.7',\
    install_requires=[
            'lxml',
            'scispacy',
            'negspacy',
    ],
    dependency_links=[
        "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_md-0.4.0.tar.gz"
    ],
    entry_points={  
        'console_scripts': [
            'clinproc=clinproc:main',
        ],
    },

    project_urls={  
        'Bug Reports': 'https://github.com/semajyllek/clinproc/issues',
        'Source': 'https://github.com/semajyllek/clinproc/',
    }
)

