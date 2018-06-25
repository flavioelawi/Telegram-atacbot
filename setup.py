#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


packages = [
    'atacbot',
]

package_data = {
}

requires = [
    "pyTelegramBotAPI",
    "configparser"
]

classifiers = [
        'Development Status :: 1 - Release',
        'Environment :: Shell',
        'License ::GPL2',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
]

setup(
    name='atacbot',
    description='Atacbot python package.',
    packages=packages,
    package_data=package_data,
    install_requires=requires,
    author="Flavio Elawi",
    author_email='flavio.elawi@gmail.com',
    url='https://github.com/flavioelawi/Telegram-atacbot',
    license='GPL',
    classifiers=classifiers,
    entry_points={
    'console_scripts': [
        'atacbot = atacbot.atacbot:main'
        ]
    }
)