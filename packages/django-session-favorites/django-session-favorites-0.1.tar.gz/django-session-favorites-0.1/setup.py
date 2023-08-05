#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


def get_readme():
    """Return the README file contents. Supports text,rst, and markdown"""
    for name in ('README', 'README.rst', 'README.md'):
        if os.path.exists(name):
            return read_file(name)
    return ''

# Use the docstring of the __init__ file to be the description
DESC = " ".join(__import__('session_favorites').__doc__.splitlines()).strip()

setup(
    name="django-session-favorites",
    version=__import__('session_favorites').get_version().replace(' ', '-'),
    url='',
    author='Arseny Sysolyatin',
    author_email='arseny.sysolyatin@gmail.com',
    description=DESC,
    long_description=get_readme(),
    packages=find_packages(exclude=['example', ]),
    include_package_data=True,
    install_requires=read_file('requirements.txt'),
    classifiers=[
        'Framework :: Django',
    ],
)
