# -*- coding: utf-8 -*-
#
#   email.py — Helper class for sending email
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
Holds helper class for sending email.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import logging
import smtplib

from debexpo.lib.base import *

log = logging.getLogger(__name__)

class Email(object):
    def __init__(self, template):
        """
        Class constructor. Sets useful class and template attributes.

        ``template``
            Name of the template to use for the email.
        """
        self.template = template
        self.server = config['global_conf']['smtp_server']
        self.auth = None
        c.sender = '%s <%s>' % (config['debexpo.sitename'], config['debexpo.email'])

        # Look whether auth is required.
        if 'smtp_username' in config['global_conf'] and 'smtp_password' in config['global_conf']:
            if config['global_conf']['smtp_username'] != '' and config['global_conf']['smtp_password'] != '':
                self.auth = {
                    'username' : config['global_conf']['smtp_username'],
                    'password' : config['global_conf']['smtp_password']
                }

    def send(self, recipients=None):
        """
        Sends the email.

        ``recipients``
            List of email addresses of recipients.
        """
        if recipients is None:
            return

        log.debug('Getting mail template: %s' % self.template)
        c.to = ', '.join(recipients)
        message = render('/email/%s.mako' % self.template)

        log.debug('Starting SMTP session to %s' % self.server)
        session = smtplib.SMTP(self.server)

        if self.auth:
            log.debug('Authentication requested; logging in')
            session.login(self.auth['user'], self.auth['password'])

        log.debug('Sending email to %s' % ', '.join(recipients))
        result = session.sendmail(config['debexpo.email'], recipients, message)

        if result:
            # Something went wrong.
            for recipient in result.keys():
                log.critical('Failed sending to %s: %s, %s' % (recipient, result[recipient][0],
                    result[recipient][1]))
        else:
            log.debug('Successfully sent')
