#!/usr/bin/env python

# ----------------------------------------------------------------------------
# Copyright (c) 2016--, Empress development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------
from glob import glob
from setuptools import setup

extensions = []

classes = """
    Development Status :: 2 - Pre-Alpha
    License :: OSI Approved :: BSD License
    Topic :: Software Development :: Libraries
    Topic :: Scientific/Engineering
    Topic :: Scientific/Engineering :: Bio-Informatics
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3 :: Only
    Operating System :: Unix
    Operating System :: POSIX
    Operating System :: MacOS :: MacOS X
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

description = ('Phylogenetic visualizations')

with open('README.md') as f:
    long_description = f.read()

# version parsing from __init__ pulled from Flask's setup.py
# https://github.com/mitsuhiko/flask/blob/master/setup.py
version = "0.0.2"

setup(
    name='empress',
    version=version,
    license='BSD',
    description=description,
    long_description=long_description,
    author="empress development team",
    author_email="cantrell.kalen@gmail.com",
    maintainer="empress development team",
    maintainer_email="cantrell.kalen@gmail.com",
    packages=['empress'],
    scripts=glob('scripts/empress'),
    package_data={
        'empress': ['tree_with_webgl.html',
                    'support_files/vendor/js/*.js',
                    'support_files/vendor/css/*.css',
                    'support_files/css/*.css',
                    'support_files/js/*.js']},
    setup_requires=['numpy >= 1.9.2'],
    ext_modules=extensions,
    install_requires=[
        'IPython >= 3.2.0',
        'matplotlib >= 1.4.3',
        'numpy >= 1.9.2',
        'pandas >= 0.18.0',
        'scipy >= 0.15.1',
        'nose >= 1.3.7',
        'scikit-bio==0.5.1',
        'tornado==4.4.2',
        'click >= 6.7'
    ],
    classifiers=classifiers,
)
