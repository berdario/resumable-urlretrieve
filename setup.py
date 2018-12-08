#! /usr/bin/env python

import sys
from setuptools import setup # type: ignore

requires = ['requests >= 2.20.0']

if sys.version_info < (3, 5):
    requires.append('typing')


setup(
    name='resumable-urlretrieve',
    version='0.1.6',
    description='Small library to fetch files over HTTP and resuming their download',
    author='Dario Bertini',
    author_email='berdario+pypi@gmail.com',
    url='https://github.com/berdario/resumable-urlretrieve',
    license='MIT License',
    packages=['resumable'],
    install_requires=requires,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP']
)
