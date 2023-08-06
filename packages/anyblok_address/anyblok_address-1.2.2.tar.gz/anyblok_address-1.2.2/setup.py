# This file is a part of the AnyBlok / Address project
#
#    Copyright (C) 2018 Franck Bret <f.bret@sensee.com>
#    Copyright (C) 2018 Hugo Quezada <h.quezada@sensee.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
# -*- coding: utf-8 -*-
"""Setup script for anyblok_address"""

from setuptools import setup, find_packages
import os

version = '1.2.2'
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'),
          'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(os.path.join(here, 'CHANGELOG.rst'),
          'r', encoding='utf-8') as changelog_file:
    changelog = changelog_file.read()

requirements = [
    'anyblok',
    'anyblok_mixins',
    'pycountry',
    'phonenumbers',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='anyblok_address',
    version=version,
    description="Address management",
    long_description=readme + '\n\n' + changelog,
    author="Franck Bret, Hugo Quezada",
    author_email='f.bret@sensee.com, h.quezada@sensee.com',
    url='http://docs.anyblok-address.anyblok.org/' + version,
    packages=find_packages(),
    entry_points={
        'bloks': [
            'address=anyblok_address.bloks.address:AddressBlok',
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='anyblok_address',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
