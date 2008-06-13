# -*- coding: utf-8 -*-
#
#   repository.py — Class to handle the repository
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
This module holds the Repository class to handle the repository.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import os
from debian_bundle import deb822
from sqlalchemy import select
import gzip
import bz2

from debexpo.lib.utils import get_package_dir
from debexpo.model import meta
from debexpo.model.package_files import PackageFile
from debexpo.model.source_packages import SourcePackage
from debexpo.model.package_versions import PackageVersion

class Repository(object):
    """
    Class to handle the repository.
    """
    def __init__(self, repository):
        """
        Class constructor. Sets the repository base directory variable.
        """
        self.repository = repository

    def _dsc_to_sources(self, package_file):
        """
        Reads the contents of a dsc file and converts it to a Sources file entry.

        ``file``
            Filename of the dsc to read.
        """
        filename = os.path.join(self.repository, package_file.filename)
        package_version = package_file.source_package.package_version
        package = package_version.package

        # Read the dsc file.
        dsc = deb822.Dsc(file(filename))

        # There are a few differences between a dsc file and a Sources entry, listed and acted
        # upon below:

        # Firstly, the "Source" field in the dsc is simply renamed to "Package".
        dsc['Package'] = dsc.pop('Source')

        # There needs to be a "Directory" field to tell the package manager where to download the
        # package from. This is in the format (for the test package in the component "main"):
        #   pool/main/t/test
        dsc['Directory'] = 'pool/%s/%s' % (package_version.component, get_package_dir(package.name))

        # The dsc file, its size, and its md5sum needs to be added to the "Files" field. This is
        # unsurprisingly not in the original dsc file!
        dsc['Files'].append({'md5sum' : package_file.md5sum, 'size': package_file.size, 'name' : package_file.filename.split('/')[-1]})

        # Get a nice rfc822 output of this dsc, now Sources, entry.
        return dsc.dump()


    def _get_sources_file(self, distribution, component):
        """
        Does a query to find all packages that fit the criteria of distribution
        and component and returns the contents of a Sources file.

        ``distribution``
            Name of the distribution to look at.

        ``component``
            Name of the component to look at.
        """
        # Get all PackageFile instances...
        dscfiles = meta.session.query(PackageFile)

        # ...include only *.dsc files...
        dscfiles = dscfiles.filter(PackageFile.filename.like('%.dsc'))

        # ...where there is a SourcePackage instance...
        dscfiles = dscfiles.filter(PackageFile.source_package_id == SourcePackage.id)

        # ...where there is a PackageVersion instance...
        dscfiles = dscfiles.filter(SourcePackage.package_version_id == PackageVersion.id)

        # ...include only packages in the specified component...
        dscfiles = dscfiles.filter(PackageVersion.component == component)

        # ...include only package in the specified distribution...
        dscfiles = dscfiles.filter(PackageVersion.distribution == distribution)

        # ...and finally create a list of PackageFile instances.
        dscfiles = dscfiles.all()

        entries = []

        # Loop through dsc files.
        for file in dscfiles:
            entries.append(self._dsc_to_sources(file))

        # Each entry is simply joined by a blank newline, so do just that to create
        # the finished Sources file.
        return '\n'.join(entries)

    def _append_current_distributions(self, distributions):
        """
        Take a look at the current directory layout and add distribution - component
        entries to the ``distributions`` dict. This is useful as if the contents of the
        Sources file is empty then the file is deleted. If a package has no longer present
        but still exists in the current Sources file, this process will remove it.
        """
        # The first time the repository dists files are generated, the dists directory
        # isn't present.
        if not os.path.isdir(os.path.join(self.repository, 'dists')):
            return distributions

        dists = os.listdir(os.path.join(self.repository, 'dists'))

        # Components are subdirectories in distribution directories.
        for dist in dists:
            components = os.listdir(os.path.join(self.repository, 'dists', dist))
            if distributions.has_key(dist):
                # The distribution already exists in the dictionary.
                for component in components:
                    if distributions[dist].count(component) == 0:
                        distributions[dist].append(component)
            else:
                # The distribution doesn't already exist in the dictionary.
                distributions[dist] = components

        return distributions

    def _get_distributions_components(self):
        """
        Return a dictionary of distribution and components in the distribution::

            { distribution1 : [ component1, component2, ... ],
              distribution2 : ... }
        """
        # Get distinct distributions from package_versions.
        packages = meta.engine.execute(select([PackageVersion.c.distribution]).distinct())

        distributions = {}

        for package in packages.fetchall():
            distributions[package[0]] = []

            components = meta.engine.execute(select([PackageVersion.c.component], PackageVersion.c.distribution == package[0]).distinct())

            for comp in components.fetchall():
                distributions[package[0]].append(comp[0])

        return self._append_current_distributions(distributions)

    def _check_directories(self, dist, component, arch=None):
        """
        Checks whether the directories needed for a dists file are present, and if not
        it creates them.

        ``dist``
            Name of the distribution.

        ``component``
            Name of the component within the distribution.

        ``arch``
            Architecture of the dists file. This defaults to *source*.
        """
        dir = self.repository

        # Default to source, otherwise binary-%(arch)s.
        if arch is None:
            arch = 'source'
        else:
            arch = 'binary-%s' % arch

        # Check each subdirectory of the dists directory.
        for dirname in ['dists', dist, component, arch]:
            dir = os.path.join(dir, dirname)

            if not os.path.isdir(dir):
                os.mkdir(dir)

    def update_sources(self):
        """
        Updates all the Sources.{gz,bz2} files for all distributions and components
        by looking at all source packages.
        """
        compression = [(gzip.GzipFile, 'gz'), (bz2.BZ2File, 'bz2')]

        # Get distributions and components.
        dists = self._get_distributions_components()

        for dist, components in dists.iteritems():
            for component in components:
                # Make sure all directories are present.
                self._check_directories(dist, component)

                # Create Sources file content.
                sources = self._get_sources_file(dist, component)
                filename = os.path.join(self.repository, 'dists', dist, component, 'source', 'Sources')

                # If the Sources file is empty, remove Sources.{gz,bz2} files. This way the
                # directory will be removed on a clean-up as it is empty.
                if sources == '':
                    for format, extension in compression:
                        if os.path.isfile('%s.%s' % (filename, extension)):
                            os.remove('%s.%s' % (filename, extension))
                else:
                    for format, extension in compression:
                        # Create the Sources files.
                        f = format('%s.%s' % (filename, extension), 'w')
                        f.write(sources)
                        f.close()
