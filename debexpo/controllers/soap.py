# -*- coding: utf-8 -*-
#
#   soap.py — soap controller
#
#   This file is part of debexpo - http://debexpo.workaround.org
#
#   Copyright © 2008 Jonny Lamb <jonnylamb@jonnylamb.com
#
#   Permission is hereby granted, free of charge, to any person
#   obtaining a copy of this software and associated documentation
#   files (the "Software"), to deal in the Software without
#   restriction, including without limitation the rights to use,
#   copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following
#   conditions:
#
#   The above copyright notice and this permission notice shall be
#   included in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#   HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#   WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#   OTHER DEALINGS IN THE SOFTWARE.

"""
Holds the SOAP controller.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import logging

from debexpo.lib.base import *
from debexpo.controllers.packages import PackagesController

from debexpo.model.users import User
from debexpo.model.packages import Package
from debexpo.model.package_versions import PackageVersion

from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Array

log = logging.getLogger(__name__)

class DebexpoService(SimpleWSGISoapApp):

    def _get_packages(self, package_filter=None, package_version_filter=None, email=None):
        """
        Helper method to construct the list for package information.
        """
        pkg_ctl = PackagesController()

        if email is not None:
            user = pkg_ctl._get_user(email)
            if user is None:
                return []
            package_filter = (Package.user_id == user.id)

        packages = pkg_ctl._get_packages(package_filter=package_filter,
            package_version_filter=package_version_filter)

        out = []
        for item in packages:
            out.append([item['name'], item['version'],
                item['uploader'], item['description'],
                config['debexpo.server'] + h.rails.url_for('package', packagename=item['name'])])

        return out

    @soapmethod(String, _returns=Array(Array(String)))
    def uploader(self, email):
        """
        Return package list filtered on uploader.
        """
        return self._get_packages(email=email)

    @soapmethod(String, _returns=Array(Array(String)))
    def section(self, section):
        """
        Return package list filtered on section.
        """
        return self._get_packages(package_version_filter=(PackageVersion.section == section))

    @soapmethod(String, _returns=Array(Array(String)))
    def maintainer(self, email):
        """
        Return package list filtered on maintainer.
        """
        return self._get_packages(package_version_filter=(PackageVersion.maintainer == email))

    @soapmethod(_returns=Array(Array(String)))
    def packages(self):
        """
        Return package list.
        """
        return self._get_packages()

SoapController = DebexpoService()
