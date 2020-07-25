# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_dird_client.commands.backends import BackendsCommand


class OdooCommand(BackendsCommand):

    resource = 'backends/odoo/sources'
