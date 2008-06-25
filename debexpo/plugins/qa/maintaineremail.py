# -*- coding: utf-8 -*-
#
#   maintaineremail.py — maintaineremail plugin
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
Holds the maintaineremail plugin.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import logging
import os
import re

from debexpo.lib import constants
from debexpo.lib.base import *
from debexpo.plugins import BasePlugin

from debexpo.model import meta
from debexpo.model.users import User

log = logging.getLogger(__name__)

class MaintainerEmailPlugin(BasePlugin):
    tests = ['test_maintainer_email']

    def test_maintainer_email(self):
        """
        Tests whether the maintainer email is the same as the uploader email.
        """
        if self.user_id is not None:
            log.debug('Checking whether the maintainer email is the same as the uploader email')

            user = meta.session.query(User).get(self.user_id)

            if user is not None:
                email = re.compile(r'^(.*) ?(<.+@.+>)$').match(self.changes['Maintainer']).group(2)

                if user.email == email[1:-1]:
                    log.debug('Maintainer email is the same as the uploader')
                    return [self.passed(__name__, 'Maintainer email is the same as the uploader', constants.PLUGIN_SEVERITY_INFO)]
                else:
                    log.warning('%s != %s' % (user.email, email[1:-1]))
                    return [self.failed(__name__, 'Changes file is not GPG signed', constants.PLUGIN_SEVERITY_WARNING)]

        log.warning('Could not get the uploader\'s user details from the database')

plugin = MaintainerEmailPlugin
