# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo.mallow import fields
from xivo.mallow.validate import Length
from xivo.mallow_helpers import ListSchema as _ListSchema
from wazo_dird.schemas import BaseSourceSchema


class SourceSchema(BaseSourceSchema):
    server = fields.String(required=True)
    port = fields.String(required=True)
    userid = fields.String(required=True)
    password = fields.String(required=True)
    database = fields.String(required=True)


class ListSchema(_ListSchema):

    searchable_columns = ['uuid', 'name', 'file']
    sort_columns = ['name', 'file']
    default_sort_column = 'name'

    recurse = fields.Boolean(missing=False)


source_list_schema = SourceSchema(many=True)
source_schema = SourceSchema()
list_schema = ListSchema()
