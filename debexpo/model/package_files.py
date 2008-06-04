# -*- coding: utf-8 -*-
#
#   package_files.py — package_files table model
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

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import sqlalchemy as sa
from sqlalchemy import orm

from debexpo.model import meta
from debexpo.model.binary_packages import BinaryPackage
from debexpo.model.source_packages import SourcePackage

t_package_files = sa.Table('package_files', meta.metadata,
    sa.Column('id', sa.types.Integer, primary_key=True),
    sa.Column('binary_package_id', sa.types.Integer, sa.ForeignKey('binary_packages.id'), nullable=True),
    sa.Column('source_package_id', sa.types.Integer, sa.ForeignKey('source_packages.id'), nullable=True),
    sa.Column('filename', sa.types.String(200), nullable=False),
    )

class PackageFile(object):
    def __init__(self, filename, binary_package=None, source_package=None):
        if binary_package is None and source_package is None:
            raise ArgumentError('binary_package AND source_package cannot both be None')

        if binary_package is not None and source_package is not None:
            raise ArgumentError('binary_package AND source_package cannot both be set')

        self.filename = filename
        self.binary_package = binary_package
        self.source_package = source_package

orm.mapper(PackageFile, t_package_files, properties={
    'binary_package' : orm.relation(BinaryPackage),
    'source_package' : orm.relation(SourcePackage),
})
