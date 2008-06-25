# -*- coding: utf-8 -*-
#
#   plugins.py — Plugin loader
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
Holds the plugin loader.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import logging
import os
import tempfile
import shutil

from debexpo.lib.base import *

log = logging.getLogger(__name__)

# Different plugin stages and their options.
plugin_stages = {
    'post-upload' : {
        'extract' : False,
    },
    'qa' : {
        'extract' : True,
    }
}

class Plugins(object):

    def __init__(self, type, changes, changes_file, user_id=None):
        """
        Class constructor. Sets class attributes and then runs the plugins.

        ``type``
            Type of plugins to run. (E.g. "post-upload")

        ``changes``
            Changes class for the package to test.

        ``changes_file``
            Name of the changes file.

        ``user_id``
            User ID of the uploader.
        """
        self.type = type.replace('-', '_')
        self.changes = changes
        self.changes_file = changes_file
        self.user_id = user_id
        self.result = None
        self.tempdir = None

        # Run the plugins.
        if type in plugin_stages:
            self.conf = plugin_stages[type]
            self.result = self._run_plugins()

    def _import_plugin(self, name):
        """
        Imports a module and returns it.

        This method was stolen from:
            http://docs.python.org/lib/built-in-funcs.html

        ``name``
            Module to import.
        """
        try:
            mod = __import__(name)
            components = name.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
            return mod
        except ImportError:
            return None

    def _extract(self):
        """
        Copy the files to a temporary directory and run dpkg-source -x on the dsc file
        to extract them.
        """
        self.tempdir = tempfile.mkdtemp()
        for file in self.changes.get_files():
            shutil.copy(os.path.join(config['debexpo.upload.incoming'], file), self.tempdir)
        shutil.copy(os.path.join(config['debexpo.upload.incoming'], self.changes_file), self.tempdir)

        self.oldcurdir = os.path.abspath(os.path.curdir)
        os.chdir(self.tempdir)

        os.system('dpkg-source -x %s extracted' % self.changes.get_dsc())

    def _cleanup(self):
        """
        Remove the previously-created temporary directory and chdir back to where the importer
        was.
        """
        if self.tempdir is not None:
            shutil.rmtree(self.tempdir)
            os.chdir(self.oldcurdir)

    def _run_plugins(self):
        """
        Look in the config file and run the plugins.
        """
        plugins = config.get('debexpo.plugins.' + self.type)
        result = []

        if plugins is None or plugins == '':
            return result

        # Look at whether the plugins need extracting.
        if self.conf['extract']:
            self._extract()

        # Run each plugin.
        for plugin in plugins.split(' '):
            name = 'debexpo.plugins.%s.%s' % (self.type.replace('_', ''), plugin)
            module = self._import_plugin(name)

            if hasattr(module, 'plugin'):
                p = getattr(module, 'plugin')(changes=self.changes, \
                    changes_file=self.changes_file, tempdir=self.tempdir,
                    user_id=self.user_id)

                result.extend(p.run())

        if self.conf['extract']:
            self._cleanup()

        return result

    def stop(self):
        """
        Returns whether the importer should stop.
        """
        for result in self.result:
            if result.stop():
                return True

        return False
