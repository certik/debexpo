# -*- coding: utf-8 -*-
#
#   validators.py — formencode validators for debexpo
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
Holds the formencode validators for debexpo.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import formencode
import md5

from debexpo.lib.base import *

from debexpo.model import meta
from debexpo.model.users import User

class GpgKey(formencode.validators.FieldStorageUploadConverter):
    """
    Validator for an uploaded GPG key. They must with the 'BEGIN PGP PUBLIC KEY BLOCK'
    text.
    """

    def _to_python(self, value, c):
        """
        Validate the GPG key.

        ``value``
            FieldStorage uploaded file.

        ``c``
        """
        if not value.value.startswith('-----BEGIN PGP PUBLIC KEY BLOCK-----'):
            raise formencode.Invalid(_('Invalid GPG key'), value, c)

        return formencode.validators.FieldStorageUploadConverter._to_python(self, value, c)

class CurrentPassword(formencode.validators.String):
    """
    Validator for a current password depending on the session's user_id.
    """

    def _to_python(self, value, c):
        """
        Validate the password.
        """
        user = meta.session.query(User).get(session['user_id'])

        if user.password != md5.new(value).hexdigest():
            raise formencode.Invalid(_('Incorrect password'), value, c)

        return formencode.validators.String._to_python(self, value, c)

class CheckBox(formencode.validators.Int):
    """
    Validator for a checkbox. When not checked, it doesn't send, and formencode
    complains.
    """
    if_missing = None

class NewEmailToSystem(formencode.validators.Email):
    """
    Email validator class to make sure there is not another user with
    the same email address already registered.
    """
    def _to_python(self, value, c=None):
        """
        Validate the email address.

        ``value``
            Address to validate.

        ``c``
        """
        u = meta.session.query(User).filter_by(email=value)

        # c.user_id can contain a user_id that should be ignored (i.e. when the user
        # wants to keep the same email).
        if hasattr(c, 'user_id'):
            u = u.filter(User.id != c.user_id)

        u = u.first()

        if u is not None:
           raise formencode.Invalid(_('A user with this email address is already registered on the system'), value, c)

        return formencode.validators.Email._to_python(self, value, c)

class NewDebianEmailToSystem(NewEmailToSystem):
    """
    NewEmailToSystem validator class to make sure the user uses a @debian.org
    email address.
    """

    def _to_python(self, value, c):
        """
        Validate the email address.

        ``value``
            Address to validate.

        ``c``
        """
        if not value.endswith('@debian.org'):
            raise formencode.Invalid(_('You must use your debian.org email address to register'), value, c)

        return NewEmailToSystem._to_python(self, value, c)
