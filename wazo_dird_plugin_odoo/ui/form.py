# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FormField,
    FieldList,
    StringField,
)

from wazo_ui.helpers.form import BaseForm


class OdooForm(BaseForm):
    first_matched_columns = FieldList(FormField(ColumnsForm))
    format_columns = FieldList(FormField(ValueColumnsForm))
    searched_columns = FieldList(FormField(ColumnsForm))
    server = StringField(l_('Server'))
    port = StringField(l_('Port'))
    userid = StringField(l_('UserID'))
    password = StringField(l_('Password'))
    database = StringField(l_('Database'))
