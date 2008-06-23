# -*- coding: utf-8 -*-
#
#   my.py — My Controller
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
Holds the MyController and form schemas.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import formencode
import logging
import md5

from debexpo.lib.base import *
from debexpo.lib import constants
from debexpo.model import meta
from debexpo.model.users import User
from debexpo.model.user_countries import UserCountry
from debexpo.controllers.register import NewEmailToSystem

log = logging.getLogger(__name__)

class MyForm(formencode.Schema):
    """
    General schema for all forms in the controller to extend.
    """
    commit = formencode.validators.String()
    form = formencode.validators.String()

class DetailsForm(MyForm):
    """
    Schema for updating user details.
    """
    name = formencode.validators.String(not_empty=True)
    email = NewEmailToSystem(not_empty=True, allow=session['user_id'])

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

class GpgForm(MyForm):
    """
    Schema for updating the user's GPG key.
    """
    gpg = GpgKey()
    delete_gpg = formencode.validators.Int()

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

class PasswordForm(MyForm):
    """
    Schema for updating the user's password.
    """
    password_current = CurrentPassword()
    password_confirm = formencode.validators.String(min=6)
    password_new = formencode.validators.String(min=6)

    # Make sure password_new and password_confirm are the same.
    chained_validators = [
        formencode.validators.FieldsMatch('password_new', 'password_confirm')
    ]

class CheckBox(formencode.validators.Int):
    """
    Validator for a checkbox. When not checked, it doesn't send, and formencode
    complains.
    """
    if_missing = None

class OtherDetailsForm(MyForm):
    """
    Schema for updating other details: country, jabber, ircnick and status.
    """
    country = formencode.validators.Number()
    ircnick = formencode.validators.String()
    jabber = formencode.validators.String()
    status = CheckBox()

class MyController(BaseController):
    """
    Controller for handling /my.
    """
    requires_auth = True

    def __init__(self):
        """
        Class constructor. Sets common class and template attributes.
        """
        c.config = config
        self.user = None

    @validate(schema=DetailsForm(), form='index')
    def _details(self):
        """
        Handles a user submitting the details form.
        """
        self.user.name = self.form_result['name']
        self.user.email = self.form_result['email']

        meta.session.commit()

        return redirect_to(h.url_for('my', action=None))

    @validate(schema=GpgForm(), form='index')
    def _gpg(self):
        """
        Handles a user submitting the GPG form.
        """
        # Should the key be deleted?
        if self.form_result['delete_gpg'] and self.user.gpg is not None:
            self.user.gpg = None

        # Should the key be updated.
        if 'gpg' in self.form_result and self.form_result['gpg'] is not None:
            self.user.gpg = self.form_result['gpg'].value

        meta.session.commit()

        return redirect_to(h.url_for('my', action=None))

    @validate(schema=PasswordForm(), form='index')
    def _password(self):
        """
        Handles a user submitting the password form.
        """
        # Simply set password.
        self.user.password = md5.new(self.form_result['password_new']).hexdigest()
        meta.session.commit()
        return redirect_to(h.url_for('my', action=None))

    @validate(schema=OtherDetailsForm(), form='index')
    def _other_details(self):
        """
        Handles a user submitting the other details form.
        """
        # A country ID of -1 means the country shouldn't be set.
        if self.form_result['country'] == -1:
            self.user.country = None
        else:
            self.user.country_id = self.form_result['country']

        self.user.ircnick = self.form_result['ircnick']
        self.user.jabber = self.form_result['jabber']

        # Only set these values if the checkbox was shown in the form.
        if config['debexpo.debian_specific'] == 'true':
            if self.user.status != constants.USER_STATUS_DEVELOPER:
                if self.form_result['status']:
                    self.user.status = constants.USER_STATUS_MAINTAINER
                else:
                    self.user.status = constants.USER_STATUS_NORMAL

        meta.session.commit()

        return redirect_to(h.url_for('my', action=None))

    def index(self):
        """
        Controller entry point. Displays forms to change user details.
        """
        # Get User object.
        self.user = meta.session.query(User).get(session['user_id'])

        if self.user is None:
            # Cannot find user from user_id.
            return redirect_to(url_for(controller='login'))

        # A form has been submit.
        if request.method == 'POST':
            try:
                return { 'details' : self._details,
                  'gpg' : self._gpg,
                  'password' : self._password,
                  'other_details' : self._other_details
                }[request.params['form']]()
            except KeyError:
                pass

        # The template will need to look at the user details.
        c.user = self.user

        # Create the countries <option> values.
        countries = '<option value="-1"'
        if self.user.country is None:
            countries += ' selected'
        countries += '></option>'

        for country in meta.session.query(UserCountry).all():
            countries += '<option value=""'
            if self.user.country_id == country.id:
                countries += ' selected'
            countries += '>%s</option>' % country.name

        c.countries = countries

        # Toggle whether Debian developer/maintainer forms should be shown.
        if self.user.status == constants.USER_STATUS_DEVELOPER:
            c.debian_developer = True
        else:
            if self.user.status == constants.USER_STATUS_MAINTAINER:
                c.debian_maintainer = True
            else:
                c.debian_maintainer = False

        # Enable the form to show information on the user's GPG key.
        if self.user.gpg is not None:
            # TODO: Make this display the right key ID.
            c.currentgpg = '0xXXXXXX'

        return render('/my/index.mako')
