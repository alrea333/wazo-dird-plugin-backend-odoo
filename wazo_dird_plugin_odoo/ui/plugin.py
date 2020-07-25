# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.plugins.dird_sources.plugin import dird_source as bp

class Plugin(object):

    def load(self, dependencies):

        @bp.route('/test')
        def test_view():
            return "Hi!"
