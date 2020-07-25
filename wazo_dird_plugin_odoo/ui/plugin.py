# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import render_template, redirect, request, url_for
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
    HiddenField,
    SubmitField
)
from wtforms.validators import InputRequired


odoo = create_blueprint('odoo', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        OdooConfigurationView.service = OdooService(clients['wazo_dird'])
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
    submit = SubmitField()


class OdooConfigurationView(BaseIPBXHelperView):
    form = OdooSourceForm
    resource = 'odoo'

    def list(self):
        return redirect(url_for('dird_source.list'))

    @route('/new/<backend>', methods=['GET'])
    def new(self, backend):
        default = {
            'odoo_config': {}
        }
        form = self.form(backend=backend, data=default)

        return render_template(self._get_template(backend=backend),
                               form_mode='add',
                               current_breadcrumbs=self._get_current_breadcrumbs(),
                               form=form)

    def post(self):
        form = self.form()
        resources = self._map_form_to_resources_post(form)

        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self._new(form)

        try:
            self.service.create(resources)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self._new(form)

        flash('Resource has been created', 'success')
        return self._redirect_for('index')

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        config_name = 'odoo_config'

        if 'format_columns' in resource[config_name]:
            resource[config_name]['format_columns'] = {option['key']: option['value'] for option in
                                                       resource[config_name]['format_columns']}

        if 'searched_columns' in resource[config_name]:
            resource[config_name]['searched_columns'] = [option['value'] for option in
                                                         resource[config_name]['searched_columns']]

        if 'first_matched_columns' in resource[config_name]:
            resource[config_name]['first_matched_columns'] = [option['value'] for option in
                                                              resource[config_name]['first_matched_columns']]

        return resource

    def _map_resources_to_form(self, resource):
        config_name = 'odoo_config'

        resource[config_name] = resource

        if 'format_columns' in resource[config_name]:
            resource[config_name]['format_columns'] = [{'key': key, 'value': val} for (key, val) in
                                                       resource[config_name]['format_columns'].items()]

        if 'searched_columns' in resource[config_name]:
            resource[config_name]['searched_columns'] = [{'value': option} for option in
                                                         resource[config_name]['searched_columns']]

        if 'first_matched_columns' in resource[config_name]:
            resource[config_name]['first_matched_columns'] = [{'value': option} for option in
                                                              resource[config_name]['first_matched_columns']]

        form = self.form(data=resource)
        return form

    def _get_template(self, type_=None, backend=None):
        blueprint = request.blueprint.replace('.', '/')

        if not type_:
            return '{blueprint}/form/form_{backend}.html'.format(
                blueprint=blueprint,
                backend=backend
            )
        else:
            return '{blueprint}/{type_}.html'.format(
                blueprint=blueprint,
                type_=type_
            )


class OdooService:

    def __init__(self, dird_client):
        self._dird = dird_client

    def get(self, source_uuid):
        results = [source for source in self.list()['items'] if source['uuid'] == source_uuid]
        source = results[0] if len(results) else None
        backend = source['backend']

        result = self._dird.backends.get_source(backend, source_uuid)
        result.update(source)
        return result

    def create(self, source_data):
        backend = source_data['backend']
        source_data['odoo_config']['name'] = source_data['name']

        return self._dird.backends.create_source(backend, source_data['odoo_config'])
