#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re

version = ''
with open('pybpodgui_plugin_stmdiagram/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


setup(
    name='pybpod-gui-plugin-stmdiagram',
    version=version,
    description="""State machine diagrams plugin""",
    author='Ricardo Jorge Vieira Ribeiro',
    author_email='ricardo.ribeiro@research.fchampalimaud.org, ricardojvr@gmail.com',
    license='Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>',
    url='https://bitbucket.org/fchampalimaud/pybpod-gui-plugin-stmdiagram',

    include_package_data=True,
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples', 'deploy', 'reports']),
    install_requires=[
        'pydot',
    ],
)
