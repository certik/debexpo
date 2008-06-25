# -*- coding: utf-8 -*-
#
#   checkfiles.py — checkfiles plugin
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
Holds the checkfiles plugin.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import logging
import os

from debexpo.lib import constants
from debexpo.lib.base import *
from debexpo.lib.utils import md5sum
from debexpo.plugins import BasePlugin

log = logging.getLogger(__name__)

class CheckFilesPlugin(BasePlugin):

    def test_md5sum(self):
        """
        Check each file's md5sum and make sure the md5sum in the changes file is the same
        as the actual file's md5sum.
        """
        for file in self.changes['Files']:
            log.debug('Checking md5sum of %s' % file['name'])
            sum = md5sum(os.path.join(config['debexpo.upload.incoming'], file['name']))

            data = 'Changes file says md5sum of %s is: %s\n' % (file['name'], file['md5sum'])
            data += 'Actual md5sum of %s is: %s' % (file['name'], sum)

            if sum != file['md5sum']:
                log.error('%s != %s' % (sum, file['md5sum']))
                self.failed('md5sum-not-match', data, constants.PLUGIN_SEVERITY_ERROR)
            else:
                log.debug('Test passed')
                self.passed('md5sum-match', None, constants.PLUGIN_SEVERITY_INFO)

plugin = CheckFilesPlugin

outcomes = {
    'md5sum-not-match' : { 'name' : 'A package source file\'s md5sum does match its changes value' },
    'md5sum-match' : { 'name' : 'A package source file\'s md5sum matches its changes value' },
}
