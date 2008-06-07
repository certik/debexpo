# -*- coding: utf-8 -*-
#
#   binary_packages.py — binary_packages table model
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
Holds binary_packages table model.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import sqlalchemy as sa
from sqlalchemy import orm

from debexpo.model import meta
from debexpo.model.package_versions import PackageVersion

t_binary_packages = sa.Table('binary_packages', meta.metadata,
    sa.Column('id', sa.types.Integer, primary_key=True),
    sa.Column('package_version_id', sa.types.Integer, sa.ForeignKey('package_versions.id')),
    sa.Column('arch', sa.types.String(200), nullable=False),
    )

class BinaryPackage(object):
    """
    Model for a binary package.
    """

    def __init__(self, package_version, arch):
        """
        Object constructor. Sets common class fields values.
        """
        self.package_version = package_version
        self.arch = arch

orm.mapper(BinaryPackage, t_binary_packages, properties={
    'package_version' : orm.relation(PackageVersion, backref='binary_packages'),
})
