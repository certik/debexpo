# -*- coding: utf-8 -*-
#
#   removepackage.py — removepackage plugin
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
Holds the removepackage plugin.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import apt_pkg
import logging
import os

from debexpo.lib import constants
from debexpo.lib.base import *
from debexpo.plugins import BasePlugin

from debexpo.model import meta
from debexpo.model.packages import Package
from debexpo.model.package_versions import PackageVersion
from debexpo.model.source_packages import SourcePackage
from debexpo.model.binary_packages import BinaryPackage
from debexpo.model.package_files import PackageFile
from debexpo.model.package_info import PackageInfo

log = logging.getLogger(__name__)

class RemovePackagePlugin(BasePlugin):

    def _remove_package_versions(self, package_versions):
        """
        Remove a package version and all its dependant parts.

        ``package_versions``
            List of PackageVersions to remove.
        """
        for package_version in package_versions:
            source_binary = package_version.source_packages
            source_binary.extend(package_version.binary_packages)

            for source_package in source_binary:
                for package_file in source_package.package_files:
                    filename = os.path.join(config['debexpo.repository'], package_file.filename)
                    if os.path.isfile(filename):
                        log.debug('Removing package file: %s' % package_file.filename)
                        os.remove(filename)
                    else:
                        log.warning('Could not find package file: %s' % package_file.filename)

                    log.debug('Deleting package file database entry: %s' % package_file.filename)
                    meta.session.delete(package_file)

                log.debug('Deleting source package database entry')
                meta.session.delete(source_package)

            log.debug('Deleting package info')
            for info in package_version.package_info:
                meta.session.delete(info)

            log.debug('Deleting package comments')
            for comment in package_version.package_comments:
                meta.session.delete(comment)

            log.debug('Deleting package version: %s' % package_version.version)
            meta.session.delete(package_version)

    def test_remove_package(self):
        """
        Removes a package that has been uploaded to Debian.
        """
        source = self.changes['Source']
        log.debug('Checking whether package %s is in the repository' % source)

        package = meta.session.query(Package).filter_by(name=source).first()

        if package is None:
            # The package is not in the repository. This will happen the most often.
            log.debug('Package is not in the repository')
            return

        # Initialise apt_pkg
        apt_pkg.init()

        keep_package_versions = []
        for package_version in package.package_versions:
            if apt_pkg.VersionCompare(self.changes['Version'], package_version.version) < 0:
                keep_package_versions.append(package_version.version)

        if len(keep_package_versions) == 0:
            # Get rid of the whole package.
            self._remove_package_versions(package.package_versions)
            log.debug('Deleting package database entry: %s' % package.name)
            meta.session.delete(package)

        else:
            # Only remove certain package versions.
            to_delete = [x for x in package.package_versions if x not in keep_package_versions]
            self._remove_package_versions(to_delete)

        meta.session.commit()

plugin = RemovePackagePlugin

outcomes = {}
