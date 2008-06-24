# -*- coding: utf-8 -*-
#
#   package_versions.py — package_versions table model
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
Holds package_versions table model.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import sqlalchemy as sa
from sqlalchemy import orm

from debexpo.model import meta, OrmObject
from debexpo.model.packages import Package

t_package_versions = sa.Table('package_versions', meta.metadata,
    sa.Column('id', sa.types.Integer, primary_key=True),
    sa.Column('package_id', sa.types.Integer, sa.ForeignKey('packages.id')),
    sa.Column('version', sa.types.String(200), nullable=False),
    sa.Column('section', sa.types.String(200), nullable=False),
    sa.Column('distribution', sa.types.String(200), nullable=False),
    sa.Column('qa_status', sa.types.Integer, nullable=False),
    sa.Column('component', sa.types.String(200), nullable=False),
    sa.Column('closes', sa.types.String(200), nullable=True),
    sa.Column('uploaded', sa.types.DateTime, nullable=False),
    )

class PackageVersion(OrmObject):
    foreign = ['package']

orm.mapper(PackageVersion, t_package_versions, properties={
    'package' : orm.relation(Package, backref='package_versions')
})
