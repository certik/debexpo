#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   importer.py — executable script to import new packages
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
Executable script to import new packages.
"""

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
    """
    Class to handle the package that is uploaded and wants to be imported into the database.
    """

    def __init__(self, changes, ini, user_id):
        """
        Object constructor. Sets class fields to sane values.

        ``self``
            Object pointer.

        ``changes``
            Name `changes` file to import. This is given from the upload controller.

        ``ini``
            Path to debexpo configuration file. This is given from the upload controller.

        ``user_id``
            ID of the user doing the upload. This is given from the upload controller.

        """
        self.changes_file = changes
        self.ini_file = ini
        self.user_id = user_id
        self.changes = None

    def _remove_changes(self):
        """
        Removes the `changes` file.
        """
        os.remove(self.changes_file)

    def _remove_files(self):
        """
        Removes all the files uploaded.
        """
        for file in self.changes.get_files():
            os.remove(file)

        self._remove_changes()

    def _fail(self, reason, use_log=True):
        """
        Fail the upload by sending a reason for failure to the log and then remove all
        uploaded files.

        A package is `fail`ed if there is a problem with debexpo, **not** if there's
        something wrong with the package.

        ``reason``
            String of why it failed.

        ``use_log``
            Whether to use the log. This should only be False when actually loading the log fails.
            In this case, the reason is printed to stderr.
        """
        if use_log:
            log.critical(reason)
        else:
            print >> sys.stderr, reason

        self._remove_files()

        # TODO email maintainer and site admin
        sys.exit(1)

    def _reject(self, reason):
        """
        Reject the package by sending a reason for failure to the log and then remove all
        uploaded files.

        A package is `reject`ed if there is a problem with the package.

        ``reason``
            String of why it failed.
        """
        log.debug('Rejected: %s' % reason)

        self._remove_files()

        # TODO email maintainer
        sys.exit(1)

    def _setup_logging(self):
        """
        Parse the config file and create the ``log`` object for other methods to log their
        actions.
        """
        global log

        # Parse the ini file to validate it
        parser = ConfigParser.ConfigParser()
        parser.read(self.ini_file)

        # Check for the presence of [loggers] in self.ini_file
        if not parser.has_section('loggers'):
            self._fail('Config file does not have [loggers] section', use_log=False)

        logging.config.fileConfig(self.ini_file)

        # Use "name.pid" to avoid importer confusions in the logs
        logger_name = 'debexpo.importer.%s' % os.getpid()
        log = logging.getLogger(logger_name)

    def _setup(self):
        """
        Set up logging, import pylons/paste/debexpo modules, parse config file, create config
        class and chdir to the incoming directory.
        """
        self._setup_logging()

        # Look for ini file
        if not os.path.isfile(self.ini_file):
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
        if not os.path.isfile(self.changes_file):
            self._fail('Cannot find changes file')

    def _create_db_entries(self):
        """
        Create entries in the Database for the package upload.
        """
        log.info('Creating database entries')

        # Horrible imports
        from debexpo.model import meta
        from debexpo.lib.utils import parse_section, get_package_dir

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
        section, component = parse_section(self.changes.get('files')[0]['section'])

        # Get uploader's User object
        user = meta.session.query(User).filter(User.id == self.user_id).one()

        # Check whether package is already in the database
        package_query = meta.session.query(Package).filter(Package.name == self.changes.get('Source'))
        if package_query.count() is 1:
            log.info('Package %s already exists in the database' % self.changes.get('Source'))
            package = package_query.one()
        else:
            log.info('Package %s is new to the system' % self.changes.get('Source'))
            package = Package(self.changes.get('Source'), user)
            package.description = self.changes.get('Description')[2:].replace('      - ', ' - ')
            meta.session.save(package)

        # No need to check whether there is the same source name and same version as an existing
        # entry in the database as the upload controller tested whether similar filenames existed
        # in the repository. The only way this would be wrong is if the filename had a different
        # version in than the Version field in changes..
        package_version = PackageVersion(package, self.changes.get('Version'), section, self.changes.get('Distribution'),
            qa_status, component, self.changes.get('Version'))
        meta.session.save(package_version)

        source_package = SourcePackage(package_version)
        meta.session.save(source_package)

        binary_package = None

        # Add PackageFile objects to the database for each uploaded file
        for file in self.changes.get_files():
            filename = os.path.join(get_package_dir(self.changes.get('Source')), file)

            # Check for binary or source package file
            if file.endswith('.deb'):
                # Only create a BinaryPackage if there actually binary package files
                if binary_package is None:
                    binary_package = BinaryPackage(package_version, arch=file[:-4].split('_')[-1])
                    meta.session.save(binary_package)

                meta.session.save(PackageFile(os.path.join(self.changes.get('Source'), file), binary_package=binary_package))
            else:
                meta.session.save(PackageFile(os.path.join(self.changes.get('Source'), file), source_package=source_package))

        # Commit all changes to the database
        meta.session.commit()
        log.info('Committed package data to the database')

    def main(self):
        """
        Actually start the import of the package.

        Do several environment sanity checks, move files into the right place, and then
        create the database entries for the imported package.
        """
        # Set up importer
        self._setup()

        log.info('Importer started with arguments: %s' % sys.argv[1:])

        from debexpo.lib.changes import Changes

        # Try parsing the changes file, but fail if there's an error.
        try:
            self.changes = Changes(filename=self.changes_file)
        except Exception, e:
            log.debug(e.message)
            self._remove_changes()
            sys.exit(1)

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
        #if not self.post_upload(self.changes):
        #   self._remove_files()

        from debexpo.lib.utils import get_package_dir

        dest = os.path.join(self.config['debexpo.repository'], get_package_dir(self.changes.get('Source')))

        # Create source package directories if they doesn't already exist
        if not os.path.isdir('/'.join(dest.split('/')[:-1])):
            os.mkdir('/'.join(dest.split('/')[:-1]))

        if not os.path.isdir(dest):
            os.mkdir(dest)

        # Check whether the files are already present
        for file in self.changes.get_files():
            if os.path.isfile(os.path.join(dest, file)):
                self._reject('File "%s" already exists' % file)

        # Install files in repository
        for file in self.changes.get_files():
            shutil.move(file, os.path.join(dest, file))

        # Create the database rows
        self._create_db_entries()

        # Finally, remove the changes file
        self._remove_changes()

if __name__ == '__main__':

    parser = OptionParser(usage="%prog -c FILE -i FILE -u ID")
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
