# -*- coding: utf-8 -*-
#
#   package.py — Package controller
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
Holds the PackageController.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import logging
import os

from debexpo.lib.base import *
from debexpo.lib.utils import get_package_dir

from debexpo.model import meta
from debexpo.model.packages import Package
from debexpo.model.package_versions import PackageVersion
from debexpo.model.users import User
from debexpo.model.package_comments import PackageComment
from debexpo.model.package_info import PackageInfo
from debexpo.model.source_packages import SourcePackage
from debexpo.model.binary_packages import BinaryPackage
from debexpo.model.package_files import PackageFile

log = logging.getLogger(__name__)

class PackageController(BaseController):

    def index(self, packagename):
        """
        Entry point into the controller. Displays information about the package.

        ``package``
            Package name to look at.
        """

        package = meta.session.query(Package).filter_by(name=packagename).first()

        if package is None:
            return redirect_to(h.url_for('packages'))

        c.package = package
        c.config = config
        c.package_dir = get_package_dir(package.name)
        return render('/package/index.mako')
