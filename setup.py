#! /usr/bin/env python

from setuptools import setup

setup(
    name='resumable-urlretrieve',
    version='0.1.0',
    description='Small library to fetch files over HTTP and resuming their download',
    author='Dario Bertini',
    author_email='berdario+pypi@gmail.com',
    url='https://github.com/berdario/resumable-urlretrieve',
    license='MIT License',
    packages=['resumable'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP']
)
