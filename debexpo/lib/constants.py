# -*- coding: utf-8 -*-
#
#   constants.py — Application constants
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
debexpo constants.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

# User constants
USER_TYPE_NORMAL = 1
USER_TYPE_ADMIN = 2

USER_STATUS_NORMAL = 1
USER_STATUS_DEVELOPER = 2
USER_STATUS_MAINTAINER = 3

# Package constants
PACKAGE_NEEDS_SPONSOR_UNKNOWN = 1
PACKAGE_NEEDS_SPONSOR_NO = 2
PACKAGE_NEEDS_SPONSOR_YES = 3

# Plugin constants
PLUGIN_SEVERITY_INFO = 1
PLUGIN_SEVERITY_WARNING = 2
PLUGIN_SEVERITY_ERROR = 3
PLUGIN_SEVERITY_CRITICAL = 4

PLUGIN_OUTCOME_PASSED = 1
PLUGIN_OUTCOME_FAILED = 2
PLUGIN_OUTCOME_INFO = 3

# Package comments
PACKAGE_COMMENT_OUTCOME_UNREVIEWED = 1
PACKAGE_COMMENT_OUTCOME_NEEDS_WORK = 2
PACKAGE_COMMENT_OUTCOME_PERFECT = 3

PACKAGE_COMMENT_STATUS_NOT_UPLOADED = 1
PACKAGE_COMMENT_STATUS_UPLOADED = 2
