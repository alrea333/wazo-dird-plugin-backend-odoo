#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup
from setuptools import find_packages

setup(
    name='wazo_dird_plugin_odoo',
    version='0.0.2',
    description='Wazo dird plugins to search in Odoo',
    author='Wazo Authors',
    author_email='dev@wazo.community',
    url='https://github.com/sboily/wazo-dird-plugin-backend-odoo',

    packages=find_packages(),
    include_package_data=True,
    package_data={
        'wazo_dird_plugin_odoo': ['api.yml', 'ui/templates/*/*/*/*.html'],
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
        'wazo_ui.plugins': [
            'odoo = wazo_dird_plugin_odoo.ui.plugin:OdooUi'
        ],

    }
)
