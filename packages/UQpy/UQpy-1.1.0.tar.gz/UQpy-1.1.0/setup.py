#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='UQpy',
    version="1.1.0",
    url='https://github.com/SURGroup/UQpy',
    authors="Michael D. Shields, Dimitris G. Giovanis",
    author_emails="michael.shields@jhu.edu, dgiovan1@jhu.edu",
    license='MIT',
    platforms='OSX',
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"":["*.pdf"]},
    install_requires=[
        "numpy", "scipy", "chaospy", "pyDOE", "scikit-learn"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
)