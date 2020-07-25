# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import render_template,redirect
from flask_classful import route


from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.form import BaseForm
from wazo_ui.helpers.view import BaseIPBXHelperView
from flask_menu.classy import register_flaskview

from wazo_ui.plugins.dird_source.plugin import dird_source as bp
from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FormField,
    FieldList,
    StringField,
    HiddenField
)
from wtforms.validators import InputRequired


odoo = create_blueprint('odoo', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        OdooConfigurationView.register(odoo, route_base='/odoo_configuration')
        register_flaskview(odoo, OdooConfigurationView)

        core.register_blueprint(odoo)

        @bp.route('dird_sources/new/odoo', methods=['GET'])
        def odoo_create():
            return redirect("/engine/odoo_configuration/new/odoo")


class ValueColumnsForm(BaseForm):
    key = StringField(validators=[InputRequired()])
    value = StringField(validators=[InputRequired()])


class ColumnsForm(BaseForm):
    value = StringField(validators=[InputRequired()])


class OdooForm(BaseForm):
    first_matched_columns = FieldList(FormField(ColumnsForm))
    format_columns = FieldList(FormField(ValueColumnsForm))
    searched_columns = FieldList(FormField(ColumnsForm))
    server = StringField(l_('Server'))
    port = StringField(l_('Port'))
    userid = StringField(l_('UserID'))
    password = StringField(l_('Password'))
    database = StringField(l_('Database'))


class OdooSourceForm(BaseForm):
    tenant_uuid = HiddenField()
    backend = HiddenField()
    name = StringField(l_('Name'), validators=[InputRequired()])
    odoo_config = FormField(OdooForm)


class OdooConfigurationView(BaseIPBXHelperView):
    form = OdooSourceForm
    resource = 'odoo'

    @route('/new/<backend>', methods=['GET'])
    def new(self, backend):
        form = self.form(backend=backend)

        return render_template(self._get_template(backend=backend),
                               form_mode='add',
                               current_breadcrumbs=self._get_current_breadcrumbs(),
                               form=form)
