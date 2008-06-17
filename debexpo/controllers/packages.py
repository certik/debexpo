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

        of packages and their most recent versions.
        """
        # I want to use apt_pkg.CompareVersions later, so init() needs to be called.
        apt_pkg.init()

        packages = []

        packages_query = meta.session.query(Package)

        if package_filter is not None:
            packages_query = packages_query.filter(package_filter)

        # Loop through all package lists.
        for package in packages_query.all():
            # Get all package versions.
            package_versions = meta.session.query(PackageVersion).filter_by(package_id=package.id)

            if package_version_filter is not None:
                package_versions = package_versions.filter(package_version_filter)

            package_versions = package_versions.all()

            # Keep a record of the most recent package version.
            recent_package_version = None

            # Loop through each package version and...
            for package_version in package_versions:
                if recent_package_version is None:
                    recent_package_version = package_version
                else:
                    if apt_pkg.VersionCompare(recent_package_version.version, package_version.version) > 0:
                        # ...record the most recent package version.
                        recent_package_vession = package_version

            if recent_package_version is not None:
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
                    'version' : recent_package_version.version,
                    'uploader' : package.user.name,
                    'needs_sponsor' : needs_sponsor
                })

        return packages

    def _get_user(self, email):
        users = meta.session.query(User).filter_by(email=email).all()

        if len(users) != 1:
            return None

        return users[0]

    def index(self):
        """
        Entry point into the PackagesController.
        """
        # List of packages to show in the list.
        packages = self._get_packages()

        # Render the page.
        c.config = config
        c.packages = packages
        return render('/packages/index.mako')

    def section(self, id):
        """
        List of packages depending on section.
        """
        packages = self._get_packages(package_version_filter=(PackageVersion.section == id))

        c.config = config
        c.packages = packages
        c.section = id
        return render('/packages/section.mako')

    def uploader(self, id):
        """
        List of packages depending on uploader.
        """
        user = self._get_user(id)

        if user is not None:
            packages = self._get_packages(package_filter=(Package.user_id == user.id))
            username = user.name
        else:
            packages = []
            username = id

        c.config = config
        c.packages = packages
        c.username = username
        return render('/packages/uploader.mako')
