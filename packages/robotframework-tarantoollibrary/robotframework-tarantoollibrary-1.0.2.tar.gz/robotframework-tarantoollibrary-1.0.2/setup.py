"""Setup module for Robot Framework Tarantool Library package."""

# To use a consistent encoding
from codecs import open
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='robotframework-tarantoollibrary',
    version='1.0.2',
    description='A Robot Framework Tarantool Library',
    long_description=long_description,
    url='https://github.com/capibara/robotframework-tarantoollibrary',
    author='Pavel Fedorov',
    author_email='Pavel.Fedorov@nexign-systems.com',
    license='License :: OSI Approved :: Apache Software License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Framework :: Robot Framework :: Library',
    ],
    package_dir={'': 'src'},
    install_requires=['tarantool>=0.5', 'robotframework>=3.0.2'],
)