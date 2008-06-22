# -*- coding: utf-8 -*-
#
#   register.py — Register Controller
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
Holds the RegisterController.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import logging
import formencode
import md5
import random
from datetime import datetime

from debexpo.lib.base import *
from debexpo.lib import constants
from debexpo.lib.email import Email
from debexpo.model import meta
from debexpo.model.users import User

log = logging.getLogger(__name__)

class NewEmailToSystem(formencode.validators.Email):
    """
    Email validator class to make sure there is not another user with
    the same email address already registered.
    """

    def _to_python(self, value, c):
        """
        Validate the email address.

        ``value``
            Address to validate.

        ``c``
        """
        u = meta.session.query(User).filter_by(email=value).first()

        if u is not None:
           raise formencode.Invalid(_('A user with this email address is already registered on the system'), value, c)

        return formencode.validators.Email._to_python(self, value, c)

class NewDebianEmailToSystem(NewEmailToSystem):
    def _to_python(self, value, c):
        if not value.endswith('@debian.org'):
            raise formencode.Invalid(_('You must use your debian.org email address to register'), value, c)

        return NewEmailToSystem._to_python(self, value, c)

class RegisterForm(formencode.Schema):
    name = formencode.validators.String(not_empty=True)
    password = formencode.validators.String(min=6)
    password_confirm = formencode.validators.String(min=6)
    commit = formencode.validators.String()

    # Make sure password and password_confirm are the same.
    chained_validators = [
        formencode.validators.FieldsMatch('password', 'password_confirm')
    ]

class MaintainerForm(RegisterForm):
    """
    Schema for the maintainer registration form.
    """
    email = NewEmailToSystem(not_empty=True)

class SponsorForm(RegisterForm):
    """
    Schema for the sponsor registration form.
    """
    email = NewDebianEmailToSystem(not_empty=True)

class RegisterController(BaseController):

    def __init__(self):
        """
        Class constructor. Sets c.config for the templates.
        """
        c.config = config

    def index(self):
        """
        Entry point to controller. Displays the index page.
        """
        return render('/register/index.mako')

    def _send_activate_email(self, key, recipient):
        """
        Sends an activation email to the potential new user.

        ``key``
            Activation key that's already stored in the database.

        ``recipient``
            Email address to send to.
        """
        email = Email('register_activate')
        c.activate_url = 'http://' + request.host + h.url_for(action='activate', id=key)
        email.send([recipient])

    @validate(schema=MaintainerForm(), form='maintainer')
    def _maintainer_submit(self):
        """
        Handles the form submission for a maintainer account registration.
        """
        # Activation key.
        key = md5.new(str(random.random())).hexdigest()

        u = User(name=self.form_result['name'],
            email=self.form_result['email'],
            password=md5.new(self.form_result['password']).hexdigest(),
            lastlogin=datetime.now(),
            verification=key)

        meta.session.save(u)
        meta.session.commit()

        self._send_activate_email(key, self.form_result['email'])

        return render('/register/activate.mako')

    def maintainer(self):
        """
        Provides the form for a maintainer account registration.
        """
        # Has the form been submitted?
        if request.method == 'POST':
            return self._maintainer_submit()
        else:
            return render('/register/maintainer.mako')

    @validate(schema=SponsorForm(), form='sponsor')
    def _sponsor_submit(self):
        """
        Handles the form submission for a sponsor account registration.
        """
        # Activation key.
        key = md5.new(str(random.random())).hexdigest()

        u = User(name=self.form_result['name'],
            email=self.form_result['email'],
            password=md5.new(self.form_result['password']).hexdigest(),
            lastlogin=datetime.now(),
            verification=key,
            status=constants.USER_STATUS_DEVELOPER)

        meta.session.save(u)
        meta.session.commit()

        self._send_activate_email(key, self.form_result['email'])

        return render('/register/activate.mako')

    def sponsor(self):
        """
        Provides the form for a sponsor account registration.
        """
        # Has the form been submitted?
        if request.method == 'POST':
            return self._sponsor_submit()
        else:
            return render('/register/sponsor.mako')

    def activate(self, id):
        """
        Upon given a verification ID, activate an account.

        ``id``
            ID to use to verify the account.
        """
        user = meta.session.query(User).filter_by(verification=id).first()

        if user is not None:
            user.verification = None
            meta.session.commit()

        c.user = user
        return render('/register/activated.mako')
