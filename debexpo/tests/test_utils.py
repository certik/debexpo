# -*- coding: utf-8 -*-
#
#   test_utils.py — Test suite for debexpo.lib.utils
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
Test suite for debexpo.lib.utils.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

from unittest import TestCase

from debexpo.lib.utils import *

class TestUtilsController(TestCase):

    def testAllowedUpload(self):
        """
        Tests debexpo.lib.utils.allowed_upload.
        """
        t = allowed_upload

        self.assertTrue(t('foo_version.orig.tar.gz'))
        self.assertTrue(t('foo_version.tar.gz'))
        self.assertTrue(t('foo_version.changes'))
        self.assertTrue(t('foo_version.dsc'))
        self.assertTrue(t('foo_version.deb'))
        self.assertTrue(t('foo_version.diff.gz'))

        self.assertFalse(t('foo_version.etc'))
