#! /usr/bin/env python

import sys
from setuptools import setup # type: ignore

requires = ['requests']

if sys.version_info < (3, 5):
    requires.append('typing')


setup(
    name='resumable-urlretrieve',
    version='0.1.5',
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
