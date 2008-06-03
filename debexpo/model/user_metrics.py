# -*- coding: utf-8 -*-
#
#   user_metrics.py — user_metrics table model
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
from debexpo.model.users import User

t_user_metrics = sa.Table('user_metrics', meta.metadata,
    sa.Column('id', sa.types.Integer, primary_key=True),
    sa.Column('user_id', sa.types.Integer, sa.ForeignKey('users.id')),
    sa.Column('name', sa.types.Integer, nullable=False),
    sa.Column('value', sa.types.Integer, nullable=False),
    )

class UserMetric(object):
    def __init__(self, user, name, value):
        self.user = user
        self.name = name
        self.value = value

orm.mapper(UserMetric, t_user_metrics, properties={
    'user' : orm.relation(User)
})
