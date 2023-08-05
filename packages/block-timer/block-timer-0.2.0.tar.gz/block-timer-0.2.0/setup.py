#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io

from setuptools import setup

setup(
    name='block-timer',
    version='0.2.0',
    description="""Measure execution time of your code blocks""",
    long_description=io.open("README.rst", 'r', encoding="utf-8").read(),
    url='https://github.com/illagrenan/block-timer',
    license='MIT',
    author='Vasek Dohnal',
    author_email='vaclav.dohnal@gmail.com',
    packages=['block_timer'],
    install_requires=[],
    extras_require={
        ":python_version<'3.5'": ['typing'],
    },
    python_requires='~=3.4',
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent'
    ]
)
