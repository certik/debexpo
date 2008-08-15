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
from datetime import datetime
from debian_bundle import deb822
import logging
import logging.config
import os
import re
import sys
import shutil
from stat import *

from sqlalchemy import exceptions

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
        self.user = None

    def _remove_changes(self):
        """
        Removes the `changes` file.
        """
        os.remove(self.changes_file)

    def _remove_files(self):
        """
        Removes all the files uploaded.
        """
        for file in self.files:
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

#        from debexpo.lib.email import Email
#        from pylons import c
#
#        if self.user is not None:
#            email = Email('importer_fail_maintainer')
#            if 'Source' in self.changes:
#                c.package = self.changes['Source']
#            else:
#                c.package = ''
#
#            email.send([self.user.email])
#
#        email = Email('importer_fail_admin')
#        c.message = reason
#        email.send([config['debexpo.email']])

        sys.exit(1)

    def _reject(self, reason):
        """
        Reject the package by sending a reason for failure to the log and then remove all
        uploaded files.

        A package is `reject`ed if there is a problem with the package.

        ``reason``
            String of why it failed.
        """
        log.error('Rejected: %s' % reason)

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
        # Look for ini file
        if not os.path.isfile(self.ini_file):
            self._fail('Cannot find ini file')

        self._setup_logging()

        # Import debexpo root directory
        sys.path.append(os.path.dirname(self.ini_file))

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

    def _create_db_entries(self, qa):
        """
        Create entries in the Database for the package upload.
        """
        log.debug('Creating database entries')

        # Horrible imports
        from debexpo.model import meta
        from debexpo.lib.utils import parse_section, md5sum
        from debexpo.lib.plugins import Plugins
        from debexpo.lib import constants
        from pylons import c

        # Import model objects
        from debexpo.model.users import User
        from debexpo.model.packages import Package
        from debexpo.model.package_versions import PackageVersion
        from debexpo.model.source_packages import SourcePackage
        from debexpo.model.binary_packages import BinaryPackage
        from debexpo.model.package_files import PackageFile
        from debexpo.model.package_info import PackageInfo
        from debexpo.model.package_subscriptions import PackageSubscription

        # Parse component and section from field in changes
        component, section = parse_section(self.changes['files'][0]['section'])

        # Get uploader's User object
        self.user = meta.session.query(User).filter_by(id=self.user_id).filter_by(verification=None)
        if self.user is None:
            self._fail('Couldn\'t find user with id %s. Exiting.' % self.user_id)

        # Check whether package is already in the database
        package_query = meta.session.query(Package).filter_by(name=self.changes['Source'])
        if package_query.count() is 1:
            log.debug('Package %s already exists in the database' % self.changes['Source'])
            package = package_query.one()
        else:
            log.debug('Package %s is new to the system' % self.changes['Source'])
            package = Package(name=self.changes['Source'], user=self.user)
            package.description = self.changes['Description'][2:].replace('      - ', ' - ')
            meta.session.save(package)

        # No need to check whether there is the same source name and same version as an existing
        # entry in the database as the upload controller tested whether similar filenames existed
        # in the repository. The only way this would be wrong is if the filename had a different
        # version in than the Version field in changes..

        try:
            closes = self.changes['Closes']
        except KeyError:
            closes = None

        # TODO: fix these magic numbers
        if qa.stop():
            qa_status = 1
        else:
            qa_status = 0

        maintainer_matches = re.compile(r'(.*) <(.*)>').match(self.changes['Maintainer'])
        maintainer = maintainer_matches.group(2)

        package_version = PackageVersion(package=package, version=self.changes['Version'],
            section=section, distribution=self.changes['Distribution'], qa_status=qa_status,
            component=component, priority=self.changes.get_priority(), closes=closes,
            uploaded=datetime.now(), maintainer=maintainer)
        meta.session.save(package_version)

        source_package = SourcePackage(package_version=package_version)
        meta.session.save(source_package)

        binary_package = None

        # Add PackageFile objects to the database for each uploaded file
        for file in self.files:
            filename = os.path.join(self.changes.get_pool_path(), file)
            sum = md5sum(os.path.join(self.config['debexpo.repository'], filename))
            size = os.stat(os.path.join(self.config['debexpo.repository'], filename))[ST_SIZE]

            # Check for binary or source package file
            if file.endswith('.deb'):
                # Only create a BinaryPackage if there actually binary package files
                if binary_package is None:
                    binary_package = BinaryPackage(package_version=package_version, arch=file[:-4].split('_')[-1])
                    meta.session.save(binary_package)

                meta.session.save(PackageFile(filename=filename, binary_package=binary_package, size=size, md5sum=sum))
            else:
                meta.session.save(PackageFile(filename=filename, source_package=source_package, size=size, md5sum=sum))

        # Add PackageInfo objects to the database for the package_version
        for result in qa.result:
            meta.session.save(PackageInfo(package_version=package_version, from_plugin=result.from_plugin,
                outcome=result.outcome, data=result.data, severity=result.severity))

        # Commit all changes to the database
        meta.session.commit()
        log.debug('Committed package data to the database')

        subscribers = meta.session.query(PackageSubscription).filter_by(package=self.changes['Source']).filter(\
            PackageSubscription.level <= constants.SUBSCRIPTION_LEVEL_UPLOADS).all()

#        if len(subscribers) >= 0:
#            c.package = self.changes['Source']
#            c.version = self.changes['Version']
#            c.user = self.user
#            c.config = config

#            email = Email('package_uploaded')
#            email.send([s.user.email for s in subscribers])

#            log.debug('Sent out package subscription emails')

    def _orig(self):
        """
        Look to see whether there is an orig tarball present, if the dsc refers to one.
        If it is present or not necessary, this returns True. Otherwise, it returns the
        name of the file required.
        """
        dsc = deb822.Dsc(open(self.changes.get_dsc()))
        for file in dsc['Files']:
            if file['name'].endswith('orig.tar.gz'):
                if os.path.isfile(file['name']):
                    return True
                else:
                    return file['name']

        return True

    def main(self):
        """
        Actually start the import of the package.

        Do several environment sanity checks, move files into the right place, and then
        create the database entries for the imported package.
        """
        # Set up importer
        self._setup()

        log.debug('Importer started with arguments: %s' % sys.argv[1:])

        from debexpo.lib.changes import Changes
        from debexpo.lib.repository import Repository
        from debexpo.lib.plugins import Plugins

        # Try parsing the changes file, but fail if there's an error.
        try:
            self.changes = Changes(filename=self.changes_file)
        except Exception, e:
            log.error(e.message)
            self._remove_changes()
            sys.exit(1)

        self.files = self.changes.get_files()

        # Look whether the orig tarball is present, and if not, try and get it from
        # the repository.
        orig = self._orig()
        if orig is not True:
            filename = os.path.join(self.config['debexpo.repository'],
                self.changes.get_pool_path(), orig)
            if os.path.isfile(filename):
                shutil.copy(filename, self.config['debexpo.upload.incoming'])
                self.files.append(orig)
            else:
                oldorig = orig
                orig = None

        post_upload = Plugins('post-upload', self.changes, self.changes_file,
            user_id=self.user_id)
        if post_upload.stop():
            log.critical('post-upload plugins failed')
            self._remove_changes()
            sys.exit(1)

        # Check whether a post-upload plugin has got the orig tarball from somewhere.
        if orig is None:
            if self._orig():
                self.files.append(oldorig)

        # Check whether the debexpo.repository variable is set
        if 'debexpo.repository' not in self.config:
            self._fail('debexpo.repository not set')

        # Check whether debexpo.repository is a directory
        if not os.path.isdir(self.config['debexpo.repository']):
            self._fail('debexpo.repository is not a directory')

        # Check whether debexpo.repository is writeable
        if not os.access(self.config['debexpo.repository'], os.W_OK):
            self._fail('debexpo.repository is not writeable')

        qa = Plugins('qa', self.changes, self.changes_file, user_id=self.user_id)
        if qa.stop():
            self._reject('QA plugins failed the package')

        destdir = self.config['debexpo.repository']

        # Loop through parent directories in the target installation directory to make sure they
        # all exist. If not, create them.
        for dir in self.changes.get_pool_path().split('/'):
            destdir = os.path.join(destdir, dir)

            if not os.path.isdir(destdir):
                log.debug('Creating directory: %s' % destdir)
                os.mkdir(destdir)

        # Check whether the files are already present
        toinstall = []
        for file in self.files:
            if os.path.isfile(os.path.join(destdir, file)):
                if not file.endswith('orig.tar.gz'):
                    self._reject('File "%s" already exists' % file)
                else:
                    log.warning('%s is not being installed as it already exists' % file)
            else:
                toinstall.append(file)

        # Install files in repository
        for file in toinstall:
            shutil.move(file, os.path.join(destdir, file))

        # Create the database rows
        self._create_db_entries(qa)

        # Execute post-successful-upload plugins
        f = open(self.changes_file)
        changes_contents = f.read()
        f.close()
        Plugins('post-successful-upload', self.changes, self.changes_file,
            changes_contents=changes_contents)

        # Remove the changes file
        self._remove_changes()

        # Refresh the Sources/Packages files.
        log.debug('Updating Sources and Packages files')
        r = Repository(self.config['debexpo.repository'])
        r.update()

        log.debug('Done')

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
