#! /usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import sublime_api

except ImportError:
    import sys

    # https://setuptools.readthedocs.io/en/latest/setuptools.html
    from setuptools import setup

    #
    # Release process setup see:
    # https://github.com/pypa/twine
    #
    # Run pip install --user keyring
    #
    # Run on cmd.exe, not mintty.exe and then type your password when prompted
    # keyring set https://upload.pypi.org/legacy/ your-username
    #
    # Run this to build the `dist/PACKAGE_NAME-xxx.tar.gz` file
    #     rm -r ./dist && python setup.py sdist
    #
    # Run this to build & upload it to `pypi`, type addons_zz when prompted.
    #     twine upload dist/*
    #
    # All in one command:
    #     rm -r ./dist && python setup.py sdist && twine upload dist/*
    #

    install_requires=[
        'portalocker; python_version>"3.4"',
        'concurrent-log-handler; python_version>"3.4"',
    ]

    if sys.platform.startswith("win"):
        install_requires.append('pypiwin32;python_version>"3.4"'),

    setup \
    (
        name='debug_tools',
        version = '2.3.0',
        description = 'Python Distribution Logger, Debugger and Utilities',
        author = 'Evandro Coan',
        license = "GPLv3",
        url = 'https://github.com/evandrocoan/debug_tools',

        package_dir = {
            '': 'all'
        },

        packages = [
            'debug_tools',
        ],

        data_files = [
            ("", ["LICENSE.txt"]),
        ],

        # To install use: pip install -e .[full]
        extras_require = {
            'full':  ["natsort"]
        },

        install_requires = install_requires,
        long_description = open('README.md').read(),
        long_description_content_type='text/markdown',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )

