#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'pyyaml']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Otuk",
    author_email='otuk@kodeten.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Infobot is an extensible social media posting bot.  Initial version will target Mastodon and will post information on coding.",
    entry_points={
        'console_scripts': [
            'infobot=infobot.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='infobot',
    name='infobot',
    packages=find_packages(include=['infobot']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/otuk/infobot',
    version='0.1.0',
    zip_safe=False,
)
