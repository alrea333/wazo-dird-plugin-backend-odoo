# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Alexis de Lattre <alexis@via.ecp.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

from xivo_dird import BaseSourcePlugin
from xivo_dird import make_result_class
import xmlrpclib
import logging

logger = logging.getLogger(__name__)


class OdooPlugin(BaseSourcePlugin):

    def load(self, config):
        self._odoo_config = config['config']['odoo_config']
        self.name = config['config']['name']
        self.sock = xmlrpclib.ServerProxy(
            'http://%s:%s/xmlrpc/object' % (
                config['config']['odoo_config']['server'],
                config['config']['odoo_config']['port']))
        self.db = config['config']['odoo_config']['database']
        self.uid = int(config['config']['odoo_config']['userid'])
        self.pwd = config['config']['odoo_config']['password']

        unique_column = 'id'
        source_name = config['config']['name']
        format_columns = config['config'].get(self.FORMAT_COLUMNS, {})

        self._SourceResult = make_result_class(
            source_name,
            unique_column,
            format_columns,
            )

    def name(self):
        return self.name

    def search(self, term, profile=None, args=None):
        logger.debug("search term=%s profile=%s", term, profile)
        partner_ids = self.sock.execute(
            self.db, self.uid, self.pwd, 'res.partner', 'search',
            [('name', 'ilike', '%%%s%%' % term)])
        logger.debug('partner_ids=%s', partner_ids)
        res = []
        if partner_ids:
            partner_reads = self.sock.execute(
                self.db, self.uid, self.pwd, 'res.partner', 'read',
                partner_ids,
                ['name', 'phone', 'mobile', 'fax', 'email', 'parent_id',
                 'child_ids', 'function'])
            for partner in partner_reads:
                res.append({
                    'firstname': '',
                    'lastname': partner['name'],
                    'job': partner['function'] or '',
                    'phone': partner['phone'] or '',
                    'email': partner['email'] or '',
                    'entity':
                    partner['parent_id'] and partner['parent_id'][1] or '',
                    'mobile': partner['mobile'] or '',
                    'fax': partner['fax'] or '',
                    })
                if partner['child_ids']:
                    logger.debug(
                        'Partner ID %d has childrens %s',
                        partner['id'], partner['child_ids'])
                    children_reads = self.sock.execute(
                        self.db, self.uid, self.pwd, 'res.partner', 'read',
                        partner['child_ids'],
                        ['name', 'phone', 'mobile', 'fax', 'email',
                         'parent_id', 'function'])
                    for child in children_reads:
                        res.append({
                            'firstname': '',
                            'lastname': child['name'],
                            'job': child['function'] or '',
                            'phone': child['phone'] or '',
                            'email': child['email'] or '',
                            'entity':
                            child['parent_id'] and child['parent_id'][1] or '',
                            'mobile': child['mobile'] or '',
                            'fax': child['fax'] or '',
                            })
        logger.debug('res=%s' % res)
        return [self._source_result_from_content(content) for content in res]

    def first_match(self, term, args=None):
        return None

    def _source_result_from_content(self, content):
        return self._SourceResult(content)
