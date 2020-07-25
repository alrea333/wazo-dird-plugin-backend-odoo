#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name='wazo_dird_plugin_odoo',
    version='0.0.2',

    description='Wazo dird plugins to search in Odoo',

    author='Alexis de Lattre',
    author_email='alexis@via.ecp.fr',

    url='https://github.com/alexis-via/xivo-dird-plugin-backend-odoo',

    packages=find_packages(),
    include_package_data=True,
    package_data={
        'wazo_dird_plugin_odoo': ['api.yml'],
    },

    entry_points={
        'wazo_dird.backends': [
            'odoo = wazo_dird_plugin_odoo.plugin:OdooPlugin',
        ],
        'wazo_dird.views': [
            'odoo_backend = wazo_dird_plugin_odoo.plugin:OdooView',
        ],
        'dird_client.commands': [
            'odoo = wazo_dird_plugin_odoo.client.plugin:OdooCommand'
        ],
    }
)
