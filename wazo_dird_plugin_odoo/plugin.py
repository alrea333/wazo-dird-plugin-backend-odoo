# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import xmlrpc.client as xmlrpclib
import logging

from wazo_dird import BaseSourcePlugin, make_result_class
from wazo_dird.helpers import BaseBackendView

from . import http


logger = logging.getLogger(__name__)


class OdooView(BaseBackendView):

    backend = 'odoo'
    list_resource = http.OdooList
    item_resource = http.OdooItem


class OdooPlugin(BaseSourcePlugin):

    def load(self, dependencies):
        config = dependencies['config']

        self.name = config['name']
        self.sock = xmlrpclib.ServerProxy('https://%s/xmlrpc/2/object' % (config['server']))
        self.db = config['database']
        self.userid = config['userid']
        self.pwd = config['password']

        logger.info('Starting Odoo authentication')
        common = xmlrpclib.ServerProxy('https://%s/xmlrpc/2/common' % (config['server']))
        self.uid = common.authenticate(self.db, self.userid, self.pwd, {})

        unique_column = None
        format_columns = dependencies['config'].get(self.FORMAT_COLUMNS, {})
        if 'reverse' not in format_columns:
            logger.info(
                'no "reverse" column has been configured on %s will use "givenName"',
                self.name
            )
            format_columns['reverse'] = '{name}'

        self._first_matched_columns = config.get(self.FIRST_MATCHED_COLUMNS, [])
        if not self._first_matched_columns:
            logger.info(
                'no "first_matched_columns" configured on "%s" no results will be matched',
                self.name,
            )


        self._SourceResult = make_result_class(
            'odoo',
            self.name,
            unique_column,
            format_columns,
        )

    def search(self, term, args=None):
        logger.debug("search term=%s", term)
        partner_ids = self.sock.execute(
            self.db, self.uid, self.pwd, 'res.partner', 'search',
            [('name', 'ilike', '%%%s%%' % term)])
        logger.debug('partner_ids=%s', partner_ids)
        res = []
        if partner_ids:
            partner_reads = self.sock.execute(
                self.db, self.uid, self.pwd, 'res.partner', 'read',
                partner_ids,
                ['name', 'phone', 'mobile', 'email', 'parent_id',
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
                    })
                if partner['child_ids']:
                    logger.debug(
                        'Partner ID %d has childrens %s',
                        partner['id'], partner['child_ids'])
                    children_reads = self.sock.execute(
                        self.db, self.uid, self.pwd, 'res.partner', 'read',
                        partner['child_ids'],
                        ['name', 'phone', 'mobile', 'email',
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
                            })
        logger.debug('res=%s' % res)
        return [self._source_result_from_content(content) for content in res]

    def first_match(self, term, args=None):
        #models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.server))
        tabfmcolumns = ['|']
        for fmcolumn in self._first_matched_columns:
            tabfmcolumns.append((fmcolumn, '=' ,term))
        logger.info('tabfmcolumns %s', tabfmcolumns)
        #responseName = models.execute_kw(self.db, self.uid, self.pwd,
        responseName = self.sock.execute_kw(
            self.db, self.uid, self.pwd,
            'res.partner', 'search_read',
            [tabfmcolumns],
            {'fields': ['name', 'parent_id'], 'limit': 1})

        if responseName:
            logger.info('Odoo reply %s', responseName)
            response = responseName[0]['name']
            if responseName[0]['parent_id']:
                response = response + ' (' + responseName[0]['parent_id'][1] + ')'
                logger.info('response %s', response)
            return self._source_result_from_content({'name': response})

        return None

    def _source_result_from_content(self, content):
        return self._SourceResult(content)
