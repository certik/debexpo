# -*- coding: utf-8 -*-
#
#   test_upload.py — UploadController test suite.
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
UploadController test suite.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import base64
from debexpo.tests import *

class TestUploadController(TestController):

    def setUp(self):
        """
        TODO: Set up database with user(s).
        """
        pass

    def testGetRequest(self):
        """
        Tests whether requests where method != PUT are rejected with error code 405.
        """
        response = self.app.get(url_for(controller='upload', filename='testname.dsc'), expect_errors=True)

        self.assertEqual(response.status, 405)

    def testNoAuthorization(self):
        """
        Tests whether requests where the "Authorization" header is missing are rejected with
        error code 401 and whether the "WWW-Authenticate" header is sent in the response with
        the correct "realm" syntax.
        """
        response = self.app.put(url_for(controller='upload', filename='testname.dsc'), expect_errors=True)

        self.assertEqual(response.status, 401)

        authenticate = response.header('WWW-Authenticate', default=False)

        self.assertNotEqual(authenticate, False)

        self.assertTrue(authenticate.startswith('Basic realm'))

    def testFalseAuthentication(self):
        """
        Tests whether false authentication details returns a 401 error code.
        """
        emailpassword = base64.encodestring('email@email.com:wrongpassword')[:-1]

        response = self.app.put(url_for(controller='upload', filename='testname.dsc'),
            headers={'Authorization' : 'Basic %s' % emailpassword}, expect_errors=True)

        self.assertEqual(response.status, 401)

    def testTrueAuthentication(self):
        """
        Tests whether true authentication details returns a nicer error code.
        """
        emailpassword = base64.encodestring('email@email.com:password')[:-1]

        response = self.app.put(url_for(controller='upload', filename='testname.dsc'),
            headers={'Authorization' : 'Basic %s' % emailpassword}, expect_errors=True)

        self.assertNotEqual(response.status, 401)
