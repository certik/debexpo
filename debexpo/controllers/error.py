# -*- coding: utf-8 -*-
#
#   py.template — template for new .py files
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

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import os.path

import paste.fileapp
from pylons.middleware import error_document_template, media_path

from debexpo.lib.base import *

class ErrorController(BaseController):
    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.
    """

    def document(self):
        """Render the error document"""
        page = error_document_template % \
            dict(prefix=request.environ.get('SCRIPT_NAME', ''),
                 code=request.params.get('code', ''),
                 message=request.params.get('message', ''))
        return page

    def img(self, id):
        """Serve Pylons' stock images"""
        return self._serve_file(os.path.join(media_path, 'img', id))

    def style(self, id):
        """Serve Pylons' stock stylesheets"""
        return self._serve_file(os.path.join(media_path, 'style', id))

    def _serve_file(self, path):
        """Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        fapp = paste.fileapp.FileApp(path)
        return fapp(request.environ, self.start_response)
