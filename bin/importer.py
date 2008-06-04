#!/usr/bin/env python
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

from optparse import OptionParser
import ConfigParser
import logging
import logging.config
import os
import sys
import shutil

log = None

class Importer(object):
    def __init__(self, changes, ini, user_id):
        self.changes = changes
        self.ini = ini
        self.user_id = user_id
        self.ch = None

    def _remove_changes(self):
        os.remove(self.changes)

    def _remove_files(self):
        for file in self.ch.get_files():
            os.remove(file)

        self._remove_changes()

    def _fail(self, reason, use_log=True):
        if use_log:
            log.critical(reason)
        else:
            print >> sys.stderr, reason

        self._remove_files()

        # TODO email maintainer and site admin
        sys.exit(1)

    def _reject(self, reason):
        log.debug('Rejected: %s' % reason)

        self._remove_files()

        # TODO email maintainer
        sys.exit(1)

    def _setup_logging(self):
        global log

        # Parse the ini file to validate it
        parser = ConfigParser.ConfigParser()
        parser.read(self.ini)

        # Check for the presence of [loggers] in self.ini
        if not parser.has_section('loggers'):
            self._fail('Config file does not have [loggers] section', use_log=False)

        logging.config.fileConfig(self.ini)

        # Use "name.pid" to avoid importer confusions in the logs
        logger_name = 'debexpo.importer.%s' % os.getpid()
        log = logging.getLogger(logger_name)

    def _setup(self):
        self._setup_logging()

        # Look for ini file
        if not os.path.isfile(self.ini):
            self._fail('Cannot find ini file')

        # Import debexpo root directory
        sys.path.append(os.path.dirname(options.ini))

        # Import debexpo modules
        from paste.deploy import appconfig
        from pylons import config
        from debexpo.config.environment import load_environment

        # Save app config for later
        self.config = config

        # Initialize Pylons app
        conf = appconfig('config:' + options.ini)
        load_environment(conf.global_conf, conf.local_conf)

        # Change into the incoming directory
        os.chdir(self.config['debexpo.upload.incoming'])

        # Look for the changes file
        if not os.path.isfile(self.changes):
            self._fail('Cannot find changes file')

    def _create_db_entries(self):
        log.info('Creating database entries')

        # Horrible imports
        from debexpo.model import meta
        from debexpo.lib.utils import parse_section

        # Import model objects
        from debexpo.model.users import User
        from debexpo.model.packages import Package
        from debexpo.model.package_versions import PackageVersion
        from debexpo.model.source_packages import SourcePackage
        from debexpo.model.binary_packages import BinaryPackage
        from debexpo.model.package_files import PackageFile

        # TODO
        qa_status = 1

        # Parse component and section from field in changes
        section, component = parse_section(self.ch.get('files')[0]['section'])

        # Get uploader's User object
        u = meta.Session.query(User).filter(User.id == self.user_id).one()

        # Check whether package is already in the database
        package_query = meta.Session.query(Package).filter(Package.name == self.ch.get('Source'))
        if package_query.count() is 1:
            log.info('Package %s already exists in the database' % self.ch.get('Source'))
            p = package_query.one()
        else:
            log.info('Package %s is new to the system' % self.ch.get('Source'))
            p = Package(self.ch.get('Source'), u)
            p.description = self.ch.get('Description')[2:].replace('      - ', ' - ')
            meta.Session.save(p)

        # No need to check whether there is the same source name and same version as an existing
        # entry in the database as the upload controller tested whether similar filenames existed
        # in the repository. The only way this would be wrong is if the filename had a different
        # version in than the Version field in changes..
        pv = PackageVersion(p, self.ch.get('Version'), section, self.ch.get('Distribution'),
            qa_status, component, self.ch.get('Version'))
        meta.Session.save(pv)

        sp = SourcePackage(pv)
        meta.Session.save(sp)

        bp = None

        # Add PackageFile objects to the database for each uploaded file
        for file in self.ch.get_files():
            # Check for binary or source package file
            if file.endswith('.deb'):
                # Only create a BinaryPackage if there actually binary package files
                if bp is None:
                    bp = BinaryPackage(pv, arch=file[:-4].split('_')[-1])
                    meta.Session.save(bp)

                meta.Session.save(PackageFile(os.path.join(self.ch.get('Source'), file), binary_package=bp))
            else:
                meta.Session.save(PackageFile(os.path.join(self.ch.get('Source'), file), source_package=pv))

        # Commit all changes to the database
        meta.Session.commit()
        log.info('Committed package data to the database')

    def main(self):
        # Set up importer
        self._setup()

        log.info('Importer started with arguments: %s' % sys.argv[1:])

        from debexpo.lib.changes import Changes
        self.ch = Changes(filename=self.changes)

        # Check whether the debexpo.repository variable is set
        if not self.config.has_key('debexpo.repository'):
            self._fail('debexpo.repository not set')

        # Check whether debexpo.repository is a directory
        if not os.path.isdir(self.config['debexpo.repository']):
            self._fail('debexpo.repository is not a directory')

        # Check whether debexpo.repository is writeable
        if not os.access(self.config['debexpo.repository'], os.W_OK):
            self._fail('debexpo.repository is not writeable')

        # TODO: post-upload plugins here
        #if not self.post_upload(self.ch):
        #   self._remove_files()

        dest = os.path.join(self.config['debexpo.repository'], self.ch.source)

        # Create source package directory if it doesn't already exist
        if not os.path.isdir(dest):
            os.mkdir(dest)

        # Check whether the files are already present
        for file in self.ch.get_files():
            if os.path.isfile(os.path.join(dest, file)):
                self._reject('File "%s" already exists' % file)

        # Install files in repository
        for file in self.ch.get_files():
            shutil.move(file, os.path.join(dest, file))

        # Create the database rows
        self._create_db_entries()

        # Finally, remove the changes file
        self._remove_changes()

if __name__ == '__main__':

    parser = OptionParser(usage="%prog -c FILE -i FILE")
    parser.add_option('-c', '--changes', dest='changes',
                      help='Path to changes file to import',
                      metavar='FILE', default=None)
    parser.add_option('-i', '--ini', dest='ini',
                      help='Path to application ini file',
                      metavar='FILE', default=None)
    parser.add_option('-u', '--userid', dest='user_id',
                      help='''Uploader's user_id''',
                      metavar='ID')

    (options, args) = parser.parse_args()

    if not options.changes or not options.ini or not options.user_id:
        parser.print_help()
        sys.exit(0)

    i = Importer(options.changes, options.ini, options.user_id)

    i.main()
