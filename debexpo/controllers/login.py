# -*- coding: utf-8 -*-
#
#   login.py — Login controller
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
Holds the LoginController class and LoginForm schema.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import formencode
import logging
import md5
from datetime import datetime

from debexpo.lib.base import *
from debexpo.model import meta
from debexpo.model.users import User

log = logging.getLogger(__name__)

class LoginForm(formencode.Schema):
    """
    Schema for the login form.
    """
    email = formencode.validators.Email(not_empty=True)
    password = formencode.validators.String(not_empty=True)
    commit = formencode.validators.String()

class LoginController(BaseController):
    """
    Manages login requests.
    """

    def __init__(self):
        """
        Class constructor. Sets common template variables.
        """
        c.config = config

    @validate(schema=LoginForm(), form='index')
    def _login(self):
        """
        Manages submissions to the login form.
        """
        password = md5.new(self.form_result['password']).hexdigest()

        u = None
        try:
            u = meta.session.query(User).filter_by(email=self.form_result['email']).filter_by(password=password).one()
        except:
            c.message = _('Invalid email or password')
            return self.index(True)

        session['user_id'] = u.id
        session.save()

        u.lastlogin = datetime.now()
        meta.session.commit()

        if 'path_before_login' in session:
            return redirect_to(session['path_before_login'])
        else:
            return redirect_to(url_for('my', action=None))

    def index(self, get=False):
        """
        Entry point. Displays the login form.

        ``get``
            If True, display the form even if request.method is POST.
        """

        if request.method == 'POST' and get is False:
            return self._login()
        else:
            return render('/login/index.mako')
