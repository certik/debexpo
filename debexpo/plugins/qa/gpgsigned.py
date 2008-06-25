# -*- coding: utf-8 -*-
#
#   gpgsigned.py — gpgsigned plugin
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
Holds the gpgsigned plugin.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import logging
import os

from debexpo.lib import constants
from debexpo.lib.base import *
from debexpo.plugins import BasePlugin

log = logging.getLogger(__name__)

class GpgSignedPlugin(BasePlugin):
    tests = ['test_gpg_signed']

    def test_gpg_signed(self):
        """
        Check to make sure the changes file is GPG signed.
        """
        log.debug('Checking whether the changes file is GPG signed')

        f = open(self.changes_file, 'r')

        if f.read().startswith('-----BEGIN PGP SIGNED MESSAGE-----'):
            log.debug('Changes file is GPG signed')
            return [self.passed(__name__, 'Changes file is GPG signed', constants.PLUGIN_SEVERITY_INFO)]
        else:
            log.warning('Changes file is not GPG signed')
            return [self.failed(__name__, 'Changes file is not GPG signed', constants.PLUGIN_SEVERITY_WARNING)]

plugin = GpgSignedPlugin
