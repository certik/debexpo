# -*- coding: utf-8 -*-
#
#   packages.py — Packages controller
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
Holds the PackagesController class.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import logging
import apt_pkg
from sqlalchemy import exceptions

from debexpo.lib.base import *

from debexpo.model import meta
from debexpo.model.package_versions import PackageVersion
from debexpo.model.packages import Package
from debexpo.model.users import User
from debexpo.lib import constants

log = logging.getLogger(__name__)

class PackagesController(BaseController):

    def _get_packages(self, package_filter=None, package_version_filter=None):
        """
        Return a list of dictionaries with keys:

        * name -- source package name
        * description -- description of package
        * version -- latest version uploaded to repository
        * uploader -- name of uploader
        * needs_sponsor -- whether the package needs a sponsor
        * package_version_id -- the ID of the most recent package version

        of packages and their most recent versions.
        """
        # I want to use apt_pkg.CompareVersions later, so init() needs to be called.
        apt_pkg.init()

        packages = []

        log.debug('Getting package list')
        packages_query = meta.session.query(Package)

        if package_filter is not None:
            log.debug('Applying package list filter')
            packages_query = packages_query.filter(package_filter)

        # Loop through all package lists.
        for package in packages_query.all():
            # Get all package versions.
            package_versions = meta.session.query(PackageVersion).filter_by(package_id=package.id)

            if package_version_filter is not None:
                package_versions = package_versions.filter(package_version_filter)

            package_versions = package_versions.all()

            if len(package_versions) != 0:
                # The package version with the highest ID will be the most recent package version
                # uploaded, so use that.
                package_version = package_versions[-1]

                # Make needs_sponsor slightly more pretty than a number.
                needs_sponsor = {
                    constants.PACKAGE_NEEDS_SPONSOR_YES : _('Yes'),
                    constants.PACKAGE_NEEDS_SPONSOR_NO : _('No'),
                    constants.PACKAGE_NEEDS_SPONSOR_UNKNOWN : _('Unknown')
                }[package.needs_sponsor]

                # Add this package to the to-show list.
                packages.append({
                    'name' : package.name,
                    'description' : package.description,
                    'version' : package_version.version,
                    'uploader' : package.user.name,
                    'needs_sponsor' : needs_sponsor,
                    'package_version_id' : package_version.id
                })

        return packages

    def _get_user(self, email):
        return meta.session.query(User).filter_by(email=email).first()

    def index(self):
        """
        Entry point into the PackagesController.
        """
        log.debug('Main package listing requested')

        # List of packages to show in the list.
        packages = self._get_packages()

        # Render the page.
        c.config = config
        c.packages = packages
        return render('/packages/list.mako')

    def section(self, id):
        """
        List of packages depending on section.
        """
        log.debug('Package listing on section = "%s" requested' % id)

        packages = self._get_packages(package_version_filter=(PackageVersion.section == id))

        c.config = config
        c.packages = packages
        c.section = id
        return render('/packages/section.mako')

    def uploader(self, id):
        """
        List of packages depending on uploader.
        """
        log.debug('Package listing on user.email = "%s" requested' % id)

        user = self._get_user(id)

        if user is not None:
            packages = self._get_packages(package_filter=(Package.user_id == user.id))
            username = user.name
        else:
            log.warning('Could not find user')
            packages = []
            username = id

        c.config = config
        c.packages = packages
        c.username = username
        return render('/packages/uploader.mako')

    def my(self):
        """
        List of packages depending on current user logged in.
        """
        log.debug('Package listing on current user requested')

        if 'user_id' not in session:
            log.debug('Requires authentication')
            session['path_before_login'] = request.path_info
            session.save()
            return redirect_to(h.rails.url_for(controller='login'))

        details = meta.session.query(User).filter_by(id=session['user_id']).one()

        return self.uploader(details.email)

    def maintainer(self, id):
        """
        List of packages depending on the Maintainer email address.
        """
        log.debug('Package listing on package_version.maintainer = "%s" requested', id)

        packages = self._get_packages(package_version_filter=(PackageVersion.maintainer == id))

        c.config = config
        c.packages = packages
        c.maintainer = id
        return render('/packages/maintainer.mako')
