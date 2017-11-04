#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name='wazo_dird_plugin_odoo',
    version='0.1',

    description='Wazo dird plugins to search in Odoo',

    author='Alexis de Lattre',
    author_email='alexis@via.ecp.fr',

    url='https://github.com/alexis-via/xivo-dird-plugin-backend-odoo',

    packages=find_packages(),

    entry_points={
        'xivo_dird.backends': [
            'odoo = wazo_dird_plugin_odoo.odoo_plugin:OdooPlugin',
        ],
    }
)
