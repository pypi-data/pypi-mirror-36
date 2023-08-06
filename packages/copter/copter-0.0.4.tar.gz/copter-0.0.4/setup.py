# -*- coding: utf-8 -*-
#!/usr/bin/env python

from setuptools import setup, find_packages
from Cython.Build import cythonize


REQUIRED_PACKAGES = [
    'biopython==1.71',
    'deap==1.2.2'
]


with open('version.cache', 'r') as f:
    version = f.read()


setup(
    name="copter",
    version=version,
    packages=find_packages(),
    description='welcome to copter',
    url='https://github.com/kyu999/copter',
    author='kyu999',
    author_email='kyukokkyou999@gmail.com',
    maintainer='kyu999',
    maintainer_email='kyukokkyou999@gmail.com',
    platforms='Linux, Darwin',
    zip_safe=False,
    include_package_data=True,
    ext_modules = cythonize(["copter/optimizers/*.pyx"]),
    install_requires=REQUIRED_PACKAGES,
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ]
)
